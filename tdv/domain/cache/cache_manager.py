from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.domain.services.independent_services.company_service import CompanyService
    from tdv.domain.services.independent_services.contract_size_service import ContractSizeService
    from tdv.domain.services.independent_services.exchange_service import ExchangeService
    from tdv.domain.services.ticker_services.ticker_service import TickerService


class CacheManager:
    def __init__(
        self,
        db: 'DB',
        entity_cache: 'EntityCache',
        exchange_service: 'ExchangeService',
        ticker_service: 'TickerService',
        company_service: 'CompanyService',
        contract_size_service: 'ContractSizeService',
    ) -> None:
        self.__db = db

        self.__entity_cache = entity_cache

        self.__exchange_service      = exchange_service
        self.__ticker_service        = ticker_service
        self.__company_service       = company_service
        self.__contract_size_service = contract_size_service

    def init_entity_cache(self) -> None:
        with self.__db.connect as conn:
            self.__entity_cache.cache_exchanges(     self.__exchange_service.get_all_exchanges(conn))
            self.__entity_cache.cache_tickers(       self.__ticker_service.get_all_tickers(conn))
            self.__entity_cache.cache_companies(     self.__company_service.get_all_companies(conn))
            self.__entity_cache.cache_contract_sizes(self.__contract_size_service.get_all_contract_sizes(conn))
