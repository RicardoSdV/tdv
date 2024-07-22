from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING
from pandas import DataFrame
from pandas_market_calendars import get_calendar
from schedule import Scheduler
import yfinance as yf

from tdv.constants import UPDATE_OPTIONS_INTERVAL

if TYPE_CHECKING:
    from typing import *
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.domain.services.yahoo_finance_service import YahooFinanceService
    from tdv.domain.types import OptionChainsYF, Options
    from tdv.libs.log import Logger


class MARKET_EVENT(Enum):
    OPEN = 'market_open'
    CLOSE = 'market_close'


class YahooFinanceServiceProxy:
    force_requests = False

    def __init__(self, yahoo_finance_service: 'YahooFinanceService', entity_cache: 'EntityCache', logger: 'Logger') -> None:
        self.__logger = logger

        self.cache_service = entity_cache

        self.yahoo_finance_service = yahoo_finance_service

        self.__schedulers_by_exchange_name = {
            exchange.name: Scheduler()
            for exchange in self.cache_service.exchanges_by_id.values()
        }

        self.__calendars_by_exchange_name = {
            exchange.name: get_calendar(exchange.name)
            for exchange in self.cache_service.exchanges_by_id.values()
        }

        self.__init_scheduling()

    def run_pending(self) -> None:
        for scheduler in self.__schedulers_by_exchange_name.values():
            scheduler.run_pending()

    def __init_scheduling(self) -> None:
        self.__logger.debug('Initializing scheduling')
        for exchange, scheduler in self.__schedulers_by_exchange_name.items():

            if self.force_requests:
<<<<<<< Updated upstream
                logger.debug('Force scheduling indefinitely', exchange=exchange)
=======
                self.__logger.debug('Forced scheduling indefinitely', exchange=exchange)
>>>>>>> Stashed changes
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                return

            next_open = self.__get_next_market_time(exchange, MARKET_EVENT.OPEN)
            next_close = self.__get_next_market_time(exchange, MARKET_EVENT.CLOSE)

<<<<<<< Updated upstream
            if next_open < next_close:
                logger.debug(
                    'Market open right now',
=======
            if next_open < next_close and next_open < datetime.now(next_open.tzinfo):
                self.__logger.debug(
                    'Market open right now_stamp_maker',
>>>>>>> Stashed changes
                    exchange=exchange,
                    next_open=next_open,
                    next_close=next_close,
                )
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)
            else:
                self.__logger.debug(
                    'Market closed',
                    exchange=exchange,
                    next_open=next_open,
                    next_close=next_close,
                )
                self.__schedule_market_events(scheduler, next_open, self.__on_market_open, exchange)

    def __schedule_periodic_requests(self, scheduler: 'Scheduler', method: 'Callable', exchange: str) -> None:
        self.__logger.debug('Starting periodic requests', exchange=exchange)
        scheduler.every(UPDATE_OPTIONS_INTERVAL).seconds.do(method, exchange)

    @staticmethod
    def __schedule_market_events(scheduler: 'Scheduler', when: 'datetime', method: 'Callable', exchange: str) -> None:
        day, time = when.strftime('%A').lower(), when.strftime('%H:%M')
        getattr(scheduler.every(), day).at(time).do(method, scheduler, time, exchange)

    def __on_market_open(self, scheduler: 'Scheduler', next_close: 'datetime', exchange: str) -> None:
        self.__logger.debug('Market open event', exchange_name=exchange, next_close=next_close)
        self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
        self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)

    def __on_market_close(self, _: 'Scheduler', next_open: 'datetime', exchange: str) -> None:
        self.__logger.debug('Market close event', exchange=exchange, next_open=next_open)
        new_scheduler = Scheduler()
        self.__schedulers_by_exchange_name[exchange] = new_scheduler
        self.__schedule_market_events(new_scheduler, next_open, self.__on_market_open, exchange)

    def __get_next_market_time(self, exchange: str, market_event: MARKET_EVENT) -> 'datetime':
        now = datetime.utcnow()
        calendar = self.__calendars_by_exchange_name[exchange]
        schedule = calendar.schedule(start_date=now, end_date=now + timedelta(days=10), tz='UTC')
        next_time = getattr(schedule, market_event.value)[0].to_pydatetime()

        self.__logger.debug(
            'Next market time gotten',
            exchange=exchange,
            next_time=next_time,
            market_event=market_event,
        )
        return next_time

    def __update_options(self, exchange_name: str) -> None:
        self.__logger.debug('Updating options', exchange=exchange_name)

        exchange_id = None
        for exchange in self.cache_service.exchanges_by_id.values():
            if exchange.name == exchange_name:
                exchange_id = exchange.id

        if exchange_id is not None:
            for ticker in self.cache_service.tickers_by_id.values():
                if ticker.exchange_id == exchange_id:

                    expiration_date_strs: 'Tuple[str, ...]' = self.__request_expirations(ticker.name)

                    tesla_ticker = yf.Ticker(ticker.name)
                    tesla_option_chains: 'OptionChainsYF' = self.__request_options(tesla_ticker, expiration_date_strs)

                    serialized_option_chains = self.serialize_yf_option_chains(tesla_option_chains)

                    self.yahoo_finance_service.save_options(serialized_option_chains, expiration_date_strs, ticker)

                    return

    def __request_options(self, ticker: 'yf.Ticker', expirations: 'Tuple[str, ...]') -> 'OptionChainsYF':
        self.__logger.debug('Requesting options', ticker=ticker)
        return [ticker.option_chain(exp) for exp in expirations]

    def __request_expirations(self, ticker_name: str) -> 'Tuple[str, ...]':
        self.__logger.debug('Expirations requested', ticker_name=ticker_name)
        expirations = yf.Ticker(ticker_name).options
        return expirations

    @staticmethod
    def serialize_yf_option_chains(option_chains: 'OptionChainsYF') -> 'Options':
        return [
            [el.to_dict() if isinstance(el, DataFrame) else el for el in option_chain]
            for option_chain in option_chains
            if all(isinstance(el, (DataFrame, dict)) for el in option_chain)
        ]
