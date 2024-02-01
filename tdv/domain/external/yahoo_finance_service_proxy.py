from typing import Optional

from yfinance import Ticker

from tdv.constants import TESLA_TICKER_NAME
from tdv.types import Expirations, OptionChainsYF
from tdv.storage.json.option_chains_repo import OptionChainsRepo


class YFserviceProxy:

    def __init__(self) -> None:
        self.__option_chains_repo = OptionChainsRepo()

        self.__tesla_option_chains: Optional[OptionChainsYF] = None

        self.__was_saved: bool = False

    def call_updates(self) -> None:
        """ Call all updates here """
        self.__update_tesla_option_chains()

    def call_saves(self) -> None:
        """ Call all saves here """
        self.__save_tesla_option_chains()

    def __update_tesla_option_chains(self) -> None:
        self.__was_saved = False
        tesla_ticker = Ticker(TESLA_TICKER_NAME)
        expirations: Expirations = self.__request_expirations(TESLA_TICKER_NAME)
        self.__tesla_option_chains = self.__request_option_chains(tesla_ticker, expirations)

    def __save_tesla_option_chains(self) -> None:
        if not self.__was_saved:
            self.__was_saved = True
            self.__option_chains_repo.save(self.__tesla_option_chains)

    @staticmethod
    def __request_option_chains(ticker: Ticker, expirations: Expirations) -> OptionChainsYF:
        return [ticker.option_chain(exp) for exp in expirations]

    @staticmethod
    def __request_expirations(ticker_name: str) -> Expirations:
        return Ticker(ticker_name).options

    @property
    def tesla_option_chains(self) -> Optional[Expirations]:
        return self.__tesla_option_chains
