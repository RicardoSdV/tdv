from datetime import datetime, timedelta
from typing import Callable, TYPE_CHECKING, Tuple

from pandas import DataFrame
from pandas_market_calendars import get_calendar
from schedule import Scheduler
import yfinance as yf

from tdv.constants import MarketEvents, UPDATE_OPTIONS_INTERVAL

from tdv.domain.types import OptionChainsYF, Options
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)

if TYPE_CHECKING:
    from tdv.domain.services_internal.cache_service import CacheService
    from tdv.domain.services_internal.yahoo_finance_service import YahooFinanceService


class YahooFinanceServiceProxy:
    force_requests = True

    def __init__(self, yahoo_finance_service: 'YahooFinanceService', cache_service: 'CacheService') -> None:
        self.cache_service = cache_service

        self.yahoo_finance_service = yahoo_finance_service

        self.__schedulers_by_exchange_name = {
            exchange.name: Scheduler() for exchange in self.cache_service.exchanges_by_id.values()
        }

        self.__calendars_by_exchange_name = {
            exchange.name: get_calendar(exchange.name) for exchange in self.cache_service.exchanges_by_id.values()
        }

        self.__init_scheduling()

    def run_pending(self) -> None:
        for scheduler in self.__schedulers_by_exchange_name.values():
            scheduler.run_pending()

    def __init_scheduling(self) -> None:
        logger.debug('Initializing scheduling')
        for exchange, scheduler in self.__schedulers_by_exchange_name.items():

            if self.force_requests:
                logger.debug('Force scheduling indefinitely', exchange=exchange)
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                return

            next_open = self.__get_next_market_time(exchange, MarketEvents.OPEN)
            next_close = self.__get_next_market_time(exchange, MarketEvents.CLOSE)
            if next_open > next_close:
                logger.debug(
                    'Market open right now',
                    exchange=exchange,
                    next_open=next_open,
                    next_close=next_close,
                )
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)
            else:
                logger.debug(
                    'Market closed',
                    exchange=exchange,
                    next_open=next_open,
                    next_close=next_close,
                )
                self.__schedule_market_events(scheduler, next_open, self.__on_market_open, exchange)

    @staticmethod
    def __schedule_periodic_requests(scheduler: Scheduler, method: Callable, exchange: str) -> None:
        logger.debug('Starting periodic requests', exchange=exchange)
        scheduler.every(UPDATE_OPTIONS_INTERVAL).seconds.do(method, exchange)

    @staticmethod
    def __schedule_market_events(scheduler: Scheduler, when: datetime, method: Callable, exchange: str) -> None:
        day, time = when.strftime('%A').lower(), when.strftime('%H:%M')
        getattr(scheduler.every(), day).at(time).do(method, scheduler, time, exchange)

    def __on_market_open(self, scheduler: Scheduler, next_close: datetime, exchange: str) -> None:
        logger.debug('Market open event', exchange_name=exchange, next_close=next_close)
        self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
        self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)

    def __on_market_close(self, _: Scheduler, next_open: datetime, exchange: str) -> None:
        logger.debug('Market close event', exchange=exchange, next_open=next_open)
        new_scheduler = Scheduler()
        self.__schedulers_by_exchange_name[exchange] = new_scheduler
        self.__schedule_market_events(new_scheduler, next_open, self.__on_market_open, exchange)

    def __get_next_market_time(self, exchange: str, market_event: MarketEvents) -> datetime:
        now = datetime.utcnow()
        calendar = self.__calendars_by_exchange_name[exchange]
        schedule = calendar.schedule(start_date=now, end_date=now + timedelta(days=10))
        next_time = getattr(schedule, market_event.value)[0].to_pydatetime()
        logger.debug(
            'Next market time gotten',
            exchange=exchange,
            next_time=next_time,
            market_event=market_event,
        )
        return next_time

    def __update_options(self, exchange_name: str) -> None:
        logger.debug('Updating options', exchange=exchange_name)

        exchange_id = None
        for exchange in self.cache_service.exchanges_by_id.values():
            if exchange.name == exchange_name:
                exchange_id = exchange.id

        if exchange_id is not None:
            for ticker in self.cache_service.tickers_by_id.values():
                if ticker.exchange_id == exchange_id:

                    expiration_date_strs: Tuple[str, ...] = self.__request_expirations(ticker.name)

                    tesla_ticker = yf.Ticker(ticker.name)
                    tesla_option_chains: OptionChainsYF = self.__request_options(tesla_ticker, expiration_date_strs)

                    serialized_option_chains = self.serialize_yf_option_chains(tesla_option_chains)

                    self.yahoo_finance_service.save_options(serialized_option_chains, expiration_date_strs, ticker)

                    return

    @staticmethod
    def __request_options(ticker: yf.Ticker, expirations: Tuple[str, ...]) -> OptionChainsYF:
        logger.debug('Requesting options', ticker=ticker)
        return [ticker.option_chain(exp) for exp in expirations]

    @staticmethod
    def __request_expirations(ticker_name: str) -> Tuple[str, ...]:
        logger.debug('Expirations requested', ticker_name=ticker_name)
        expirations = yf.Ticker(ticker_name).options
        return expirations

    @staticmethod
    def serialize_yf_option_chains(option_chains: OptionChainsYF) -> Options:
        return [
            [el.to_dict() if isinstance(el, DataFrame) else el for el in option_chain]
            for option_chain in option_chains
            if all(isinstance(el, (DataFrame, dict)) for el in option_chain)
        ]
