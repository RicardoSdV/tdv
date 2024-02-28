from typing import Optional, TYPE_CHECKING

from tdv.infra.database import db
from tdv.infra.repos import repos

if TYPE_CHECKING:
    from tdv.domain.internal.exchanges_service import ExchangesService
    from tdv.domain.internal.option_chains_service import OptionChainsService
    from tdv.domain.internal.options_service import OptionsService
    from tdv.domain.internal.ticker_service import TickerService


class Services:
    def __init__(self) -> None:
        self.__exchange_service: Optional['ExchangesService'] = None
        self.__ticker_service: Optional['TickerService'] = None
        self.__option_chains_service: Optional['OptionChainsService'] = None
        self.__options_service: Optional['OptionsService'] = None

    @property
    def exchange_service(self) -> 'ExchangesService':
        if self.__exchange_service is None:
            from tdv.domain.internal.exchanges_service import ExchangesService
            self.__exchange_service = ExchangesService(db, repos.exchange_repo)
        return self.__exchange_service

    @property
    def ticker_service(self) -> 'TickerService':
        if self.__ticker_service is None:
            from tdv.domain.internal.ticker_service import TickerService
            self.__ticker_service = TickerService()
        return self.__ticker_service

    @property
    def option_chains_service(self) -> 'OptionChainsService':
        if self.__option_chains_service is None:
            from tdv.domain.internal.option_chains_service import OptionChainsService
            self.__option_chains_service = OptionChainsService()
        return self.__option_chains_service

    @property
    def options_service(self) -> 'OptionsService':
        if self.__options_service is None:
            from tdv.domain.internal.options_service import OptionsService
            self.__options_service = OptionsService()
        return self.__options_service


services = Services()
