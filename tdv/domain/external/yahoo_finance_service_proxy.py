from datetime import datetime as Datetime, timedelta
from typing import Tuple, Dict, Callable

from pandas_market_calendars import MarketCalendar, get_calendar
from schedule import Scheduler
from yfinance import Ticker

from tdv.constants import MarketEvent
from tdv.data_types import Expirations, OptionChainsYF, Second, TickerName, ExchangeName
from tdv.logger_setup import logger_obj
from tdv.storage.json.option_chains_repo import OptionChainsRepo

logger = logger_obj.get_logger(__name__)


class BaseServiceProxy:
    def run_pending(self) -> None:
        raise NotImplementedError


class YFserviceProxy(BaseServiceProxy):
    __update_options_interval: Second = 10
    __exchange_tickers: Dict[ExchangeName, Tuple[TickerName]] = {'NYSE': ('TSLA',)}
    __pretty_print_json = False

    def __init__(self) -> None:
        self.__option_chains_repo = OptionChainsRepo()

        self.__schedulers: Dict[ExchangeName, Scheduler] = {name: Scheduler() for name in self.__exchange_tickers.keys()}
        self.__calendars: Dict[ExchangeName, MarketCalendar] = {name: get_calendar(name) for name in self.__exchange_tickers.keys()}

        self.__init_scheduling()

    def run_pending(self) -> None:
        for scheduler in self.__schedulers.values():
            scheduler.run_pending()

    def __init_scheduling(self) -> None:
        """ Schedules jobs on startup to initialize scheduling chain """
        for exchange_name, scheduler in self.__schedulers.items():
            next_open = self.__get_next_market_time(exchange_name, MarketEvent.OPEN)
            next_close = self.__get_next_market_time(exchange_name, MarketEvent.CLOSE)
            print(next_open, next_close)
            if next_open > next_close:  # If next open is after next close market is open right now
                self.__schedule_periodic_requests(scheduler, self.__update_options, exchange_name)
                self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange_name)
            else:  # Market is closed
                self.__schedule_market_events(scheduler, next_open, self.__on_market_open, exchange_name)

    @classmethod
    def __schedule_periodic_requests(cls, scheduler: Scheduler, method: Callable, exchange_name: ExchangeName) -> None:
        scheduler.every(cls.__update_options_interval).seconds.do(method, exchange_name)

    @staticmethod
    def __schedule_market_events(scheduler: Scheduler, when: Datetime, method: Callable, exchange_name: ExchangeName) -> None:
        day, time = when.strftime('%A').lower(), when.strftime('%H:%M')
        print(day, time)
        getattr(scheduler.every(), day).at(time).do(method, scheduler, time, exchange_name)

    def __on_market_open(self, scheduler: Scheduler, next_close: Datetime, exchange_name: ExchangeName) -> None:
        """ On market open schedule periodic requests & market close """
        self.__schedule_periodic_requests(scheduler, self.__update_options, exchange_name)
        self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange_name)

    def __on_market_close(self, _: Scheduler, next_open: Datetime, exchange_name: ExchangeName) -> None:
        """ On market close schedule next market open """
        new_scheduler = Scheduler()
        self.__schedulers[exchange_name] = new_scheduler
        self.__schedule_market_events(new_scheduler, next_open, self.__on_market_open, exchange_name)

    def __get_next_market_time(self, exchange_name: ExchangeName, market_event: MarketEvent) -> Datetime:
        now = Datetime.utcnow()
        calendar = self.__calendars[exchange_name]
        schedule = calendar.schedule(start_date=now, end_date=now + timedelta(days=10))
        return getattr(schedule, market_event.value)[0].to_pydatetime()

    def __update_options(self, exchange_name: ExchangeName) -> None:
        """ Updates options for all tickers associated with the given exchange name.
        DISCLAIMER: Adding tickers will increase the main loop cycle time and so reduce request frequency """
        # TODO: Redo, use asyncio, download options only once, look how YF works in depth

        for ticker_name in self.__exchange_tickers[exchange_name]:
            expirations: Expirations = self.__request_expirations(ticker_name)

            tesla_ticker = Ticker(ticker_name)
            tesla_option_chains: OptionChainsYF = self.__request_options(tesla_ticker, expirations)

            self.__option_chains_repo.save(tesla_option_chains, 2 if self.__pretty_print_json else None)

    @staticmethod
    def __request_options(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
        logger.debug('Requesting options')
        return [ticker.option_chain(exp) for exp in expirations]


    @staticmethod
    def __request_expirations(ticker_name: str) -> Expirations:
        expirations = Ticker(ticker_name).options
        logger.debug('Expirations requested', ticker_name=ticker_name)
        return expirations
