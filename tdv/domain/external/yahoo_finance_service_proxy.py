import json
from datetime import datetime


from tdv.domain.entities.ticker_entity import TickersEnum
from tdv.domain.types import Second
from tdv.domain.yfinance import Ticker
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


"""
The idea is leverage yfinance threading capability in combination with proxy rotation to be able to request multiple
ticker option chains at reasonable intervals ~= 10 seconds/ticker
"""

class YFserviceProxy(Ticker):
    __update_options_interval: Second = 10

    # def __init__(self, ticker: Tickers) -> None:

        # self.__schedulers = {name: Scheduler() for name in self.__exchange_tickers.keys()}
        # self.__calendars = {name: get_calendar(name) for name in self.__exchange_tickers.keys()}
        #
        # self.__init_scheduling()

    def _download_options(self, date=None):
        if date is None:
            url = f"{self._base_url}/v7/finance/options/{self.ticker}"
        else:
            url = f"{self._base_url}/v7/finance/options/{self.ticker}?date={date}"

        r = self._data.get(url=url, proxy=self.proxy).json()
        # print('r:', json.dumps(r, indent=2))

        if len(r.get('optionChain', {}).get('result', [])) > 0:
            for exp in r['optionChain']['result'][0]['expirationDates']:
                self._expirations[datetime.utcfromtimestamp(
                    exp).strftime('%Y-%m-%d')] = exp

            self._underlying = r['optionChain']['result'][0].get('quote', {})

            opt = r['optionChain']['result'][0].get('options', [])

            return dict(**opt[0], underlying=self._underlying) if len(opt) > 0 else {}
        return {}

    def run(self) -> None:
        if self._expirations:
            for date in self._expirations:
                self._download_options(date)

        options = self._download_options()
        print('options', json.dumps(options, indent=2))
        print('self._expirations', json.dumps(self._expirations, indent=2))
        print('self._underlying', json.dumps(self._underlying, indent=2))

    # def run_pending(self) -> None:
    #     for scheduler in self.__schedulers.values():
    #         scheduler.run_pending()
    #
    # def __init_scheduling(self) -> None:
    #     logger.debug('Initializing scheduling')
    #     for exchange, scheduler in self.__schedulers.items():
    #         next_open = self.__get_next_market_time(exchange, MarketEvents.OPEN)
    #         next_close = self.__get_next_market_time(exchange, MarketEvents.CLOSE)
    #         if next_open > next_close:
    #             logger.debug('Market open right now', exchange=exchange, next_open=next_open, next_close=next_close)
    #             self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
    #             self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)
    #         else:
    #             logger.debug('Market closed', exchange=exchange, next_open=next_open, next_close=next_close)
    #             self.__schedule_market_events(scheduler, next_open, self.__on_market_open, exchange)
    #
    # @classmethod
    # def __schedule_periodic_requests(cls, scheduler: Scheduler, method: Callable, exchange: str) -> None:
    #     logger.debug('Starting periodic requests', exchange=exchange)
    #     scheduler.every(cls.__update_options_interval).seconds.do(method, exchange)
    #
    # @staticmethod
    # def __schedule_market_events(scheduler: Scheduler, when: datetime, method: Callable, exchange: str) -> None:
    #     day, time = when.strftime('%A').lower(), when.strftime('%H:%M')
    #     getattr(scheduler.every(), day).at(time).do(method, scheduler, time, exchange)
    #
    # def __on_market_open(self, scheduler: Scheduler, next_close: datetime, exchange: str) -> None:
    #     logger.debug('Market open event', exchange_name=exchange, next_close=next_close)
    #     self.__schedule_periodic_requests(scheduler, self.__update_options, exchange)
    #     self.__schedule_market_events(scheduler, next_close, self.__on_market_close, exchange)
    #
    # def __on_market_close(self, _: Scheduler, next_open: datetime, exchange: str) -> None:
    #     logger.debug('Market close event', exchange=exchange, next_open=next_open)
    #     new_scheduler = Scheduler()
    #     self.__schedulers[exchange] = new_scheduler
    #     self.__schedule_market_events(new_scheduler, next_open, self.__on_market_open, exchange)
    #
    # def __get_next_market_time(self, exchange: str, market_event: MarketEvents) -> datetime:
    #     now = datetime.utcnow()
    #     calendar = self.__calendars[exchange]
    #     schedule = calendar.schedule(start_date=now, end_date=now + timedelta(days=10))
    #     next_time = getattr(schedule, market_event.value)[0].to_pydatetime()
    #     logger.debug('Next market time gotten', exchange=exchange, next_time=next_time, market_event=market_event)
    #     return next_time
    #
    # def __update_options(self, exchange: str) -> None:
    #     """ Updates options for all tickers associated with the given exchange name.
    #     DISCLAIMER: Adding tickers will increase the main loop cycle time and so reduce request frequency """
    #     # TODO: Redo, use asyncio, download options only once, look how YF works in depth
    #     logger.debug('Updating options', exchange=exchange)
    #
    #     for ticker_name in self.__exchange_tickers[exchange]:
    #         expirations: Expirations = self.__request_expirations(ticker_name)
    #
    #         tesla_ticker = Ticker(ticker_name)
    #         tesla_option_chains: OptionChainsYF = self.__request_options(tesla_ticker, expirations)
    #
    #         self.__option_chains_repo.save(tesla_option_chains, 2 if self.__pretty_print_json else None)
    #
    # @staticmethod
    # def __request_options(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
    #     logger.debug('Requesting options', ticker=ticker)
    #     return [ticker.option_chain(exp) for exp in expirations]
    #
    # @staticmethod
    # def __request_expirations(ticker_name: str) -> Expirations:
    #     logger.debug('Expirations requested', ticker_name=ticker_name)
    #     expirations = Ticker(ticker_name).options
    #     return expirations


ticker = Ticker(TickersEnum.TSLA.value)
options = ticker._download_options()
print('options', json.dumps(options, indent=2))
print('self._expirations', json.dumps(ticker._expirations, indent=2))
print('self._underlying', json.dumps(ticker._underlying, indent=2))
