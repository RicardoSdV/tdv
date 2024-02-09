from typing import Optional

from schedule import Scheduler, Job
from yfinance import Ticker

from tdv.data_types import Expirations, OptionChainsYF, Second
from tdv.logger_setup import logger_setup
from tdv.storage.json.option_chains_repo import OptionChainsRepo

logger = logger_setup.get_logger(__name__)


class BaseServiceProxy:
    def run_pending(self) -> None:
        raise NotImplementedError


class YFserviceProxy(BaseServiceProxy):
    __update_options_interval: Second = 10
    __tesla_ticker_name = 'TSLA'
    __pretty_print_json = False

    def __init__(self) -> None:
        self.__option_chains_repo = OptionChainsRepo()

        self.__scheduler = Scheduler()

        self.__tesla_options_job: Optional[Job] = self.__schedule_tesla_options_job()

    def run_pending(self) -> None:
        self.__scheduler.run_pending()

    def __schedule_tesla_options_job(self) -> Job:
        logger.debug('Scheduling tesla options update', every=self.__update_options_interval)
        return self.__scheduler.every(self.__update_options_interval).seconds.do(self.update_tesla_options)

    def update_tesla_options(self) -> None:
        expirations: Expirations = self.__request_expirations(self.__tesla_ticker_name)

        tesla_ticker = Ticker(self.__tesla_ticker_name)  # TODO: Check if ticker needs reinitialization so often
        tesla_option_chains: OptionChainsYF = self.__request_options(tesla_ticker, expirations)

        self.__option_chains_repo.save(tesla_option_chains, 2 if self.__pretty_print_json else None)

    @staticmethod
    def __request_options(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
        options = [ticker.option_chain(exp) for exp in expirations]  # TODO: Rethink all, use inheritance, override
        logger.debug('Options requested', _ticker=ticker, options=options)
        return options

    @staticmethod
    def __request_expirations(ticker_name: str) -> Expirations:
        expirations = Ticker(ticker_name).options
        logger.debug('Request expirations', _ticker_name=ticker_name)
        return expirations
