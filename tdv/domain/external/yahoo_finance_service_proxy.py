from datetime import datetime, time
from typing import Optional

from pytz import timezone
from schedule import Scheduler, Job
from yfinance import Ticker

from tdv.data_types import Expirations, OptionChainsYF, Second
from tdv.logger_settup import logger
from tdv.storage.json.option_chains_repo import OptionChainsRepo


class BaseServiceProxy:
    def run_pending(self) -> None:
        raise NotImplementedError


class YFserviceProxy(BaseServiceProxy): # Gotta change market open and close here to the main loop version
    __work_only_when_market_open = False
    __time_zone = timezone('America/New_York')
    __market_open = time(hour=9, minute=30)
    __market_close = time(hour=16)

    __update_tesla_option_chains_interval: Second = 10
    __tesla_ticker_name = 'TSLA'
    __pretty_print = False  # Set to True to pretty print to .json

    def __init__(self) -> None:
        self.__option_chains_repo = OptionChainsRepo()

        self.__scheduler = Scheduler()

        self.__tesla_options_job: Optional[Job] = self.__schedule_tesla_options_job()

    def run_pending(self) -> None:
        self.__scheduler.run_pending()

    def __schedule_tesla_options_job(self) -> Job:
        logger.info("Tesla option chain jobs scheduled")
        return self.__scheduler.every(
            self.__update_tesla_option_chains_interval
        ).seconds.do(self.__request_and_save_tesla_option_chains)

    def __request_and_save_tesla_option_chains(self) -> None:
        expirations: Expirations = self.__request_expirations(self.__tesla_ticker_name)

        tesla_ticker = Ticker(self.__tesla_ticker_name)
        tesla_option_chains: OptionChainsYF = self.__request_option_chains(tesla_ticker, expirations)

        self.__option_chains_repo.save(tesla_option_chains, None)

    @staticmethod
    def __request_option_chains(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
        logger.info("Requested option chains for each expiration")
        return [ticker.option_chain(exp) for exp in expirations]

    @staticmethod
    def __request_expirations(ticker_name: str) -> Expirations:
        logger.info("Requested expirations")
        return Ticker(ticker_name).options
