from datetime import datetime, timedelta
from typing import Callable

from pandas import DataFrame
from pandas_market_calendars import get_calendar
from schedule import Scheduler
from yfinance import Ticker

from tdv.constants import MarketEvents
from tdv.domain.internal.yahoo_finance_service import YahooFinanceService
from tdv.domain.types import Expiries, OptionChainsYF, Second, OptionChains
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class YahooFinanceServiceProxy:
    __update_options_interval: Second = 10
    __exchange_tickers = {'NYSE': ('TSLA',)}
    force_requests = True

    def __init__(self, yahoo_finance_service: 'YahooFinanceService') -> None:
        self.yahoo_finance_service = yahoo_finance_service

        self.__schedulers = {name: Scheduler() for name in self.__exchange_tickers.keys()}
        self.__calendars = {name: get_calendar(name) for name in self.__exchange_tickers.keys()}

        self.__init_scheduling()

    def run_pending(self) -> None:
        for scheduler in self.__schedulers.values():
            scheduler.run_pending()

    def __init_scheduling(self) -> None:
        logger.debug('Initializing scheduling')
        for exchange, scheduler in self.__schedulers.items():

            if self.force_requests:
                logger.debug('Force scheduling indefinitely', exchange=exchange)
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                return

            next_open = self.__get_next_market_time(exchange, MarketEvents.OPEN)
            next_close = self.__get_next_market_time(exchange, MarketEvents.CLOSE)
            if next_open > next_close:
                logger.debug('Market open right now', exchange=exchange, next_open=next_open, next_close=next_close)
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
                self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)
            else:
                logger.debug('Market closed', exchange=exchange, next_open=next_open, next_close=next_close)
                self.__schedule_market_events(scheduler, next_open, self.__on_market_open, exchange)

    @classmethod
    def __schedule_periodic_requests(cls, scheduler: Scheduler, method: Callable, exchange: str) -> None:
        logger.debug('Starting periodic requests', exchange=exchange)
        scheduler.every(cls.__update_options_interval).seconds.do(method, exchange)

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
        self.__schedulers[exchange] = new_scheduler
        self.__schedule_market_events(new_scheduler, next_open, self.__on_market_open, exchange)

    def __get_next_market_time(self, exchange: str, market_event: MarketEvents) -> datetime:
        now = datetime.utcnow()
        calendar = self.__calendars[exchange]
        schedule = calendar.schedule(start_date=now, end_date=now + timedelta(days=10))
        next_time = getattr(schedule, market_event.value)[0].to_pydatetime()
        logger.debug('Next market time gotten', exchange=exchange, next_time=next_time, market_event=market_event)
        return next_time

    def __update_options(self, exchange: str) -> None:
        logger.debug('Updating options', exchange=exchange)

        for ticker_name in self.__exchange_tickers[exchange]:
            expiries: Expiries = self.__request_expirations(ticker_name)

            tesla_ticker = Ticker(ticker_name)
            tesla_option_chains: OptionChainsYF = self.__request_options(tesla_ticker, expiries)

            serialized_option_chains = self.serialize_yf_option_chains(tesla_option_chains)

            self.yahoo_finance_service.save_option_chains(serialized_option_chains, expiries, ticker_name)

    @staticmethod
    def __request_options(ticker: Ticker, expirations: Expiries) -> OptionChainsYF:
        logger.debug('Requesting options', ticker=ticker)
        return [ticker.option_chain(exp) for exp in expirations]

    @staticmethod
    def __request_expirations(ticker_name: str) -> Expiries:
        logger.debug('Expirations requested', ticker_name=ticker_name)
        expirations = Ticker(ticker_name).options
        return expirations

    @staticmethod
    def serialize_yf_option_chains(option_chains: OptionChainsYF) -> OptionChains:
        return [
            [el.to_dict() if isinstance(el, DataFrame) else el for el in option_chain]
            for option_chain in option_chains
            if all(isinstance(el, (DataFrame, dict)) for el in option_chain)
        ]
