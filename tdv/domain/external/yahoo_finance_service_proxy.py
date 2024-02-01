from typing import Iterable, Union, Any, Optional

from pandas import DataFrame
from yfinance import Ticker

from tdv.common_utils import timestamp
from tdv.constants import TESLA_TICKER_NAME
from tdv.types import Expirations, OptionChains, OptionChainsYF
from tdv.storage.json.option_chains_repo import OptionChainsRepo


class YFserviceProxy:

    def __init__(self) -> None:
        self.__option_chains_repo = OptionChainsRepo()

        self.__tesla_option_chains: Optional[OptionChainsYF] = None

    def call_updates(self) -> None:
        """ Call all updates here """
        self.__update_tesla_option_chains()

    def call_saves(self) -> None:
        """ Call all saves here """
        self.__save_tesla_option_chains()

    def __update_tesla_option_chains(self) -> None:
        tesla_ticker = Ticker(TESLA_TICKER_NAME)
        expirations: Expirations = self.__request_expirations(TESLA_TICKER_NAME)
        self.__tesla_option_chains = self.__request_option_chains(tesla_ticker, expirations)

    def __save_tesla_option_chains(self) -> None:
        if self.__tesla_option_chains:
            self.__option_chains_repo.save(self.__tesla_option_chains)
        self.__tesla_expirations = None

    @staticmethod
    def __request_option_chains(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
        return [ticker.option_chain(exp) for exp in expirations]

    @staticmethod
    def __request_expirations(ticker_name: str) -> Expirations:
        return Ticker(ticker_name).options

    @property
    def tesla_expirations(self) -> Optional[Expirations]:
        return self.__tesla_expirations
