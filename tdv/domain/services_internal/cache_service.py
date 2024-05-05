from typing import TYPE_CHECKING, Dict, Optional

from tdv.domain.entities.independent_entities.company_entity import Company
from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
from tdv.domain.entities.independent_entities.exchange_entity import Exchange
from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
from tdv.domain.entities.option_entities.call_hist_entity import CallHist
from tdv.domain.entities.option_entities.put_hist_entity import PutHist
from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist
from tdv.domain.entities.ticker_entities.ticker_entity import Ticker

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.services_internal.independent_services.company_service import CompanyService
    from tdv.domain.services_internal.independent_services.contract_size_service import ContractSizeService
    from tdv.domain.services_internal.independent_services.exchange_service import ExchangeService
    from tdv.domain.services_internal.ticker_services.ticker_service import TickerService


class CacheService:
    """For caching entities & more that are used in many places"""

    def __init__(
        self,
        db: 'DB',
        company_service: 'CompanyService',
        exchange_service: 'ExchangeService',
        ticker_service: 'TickerService',
        contract_size_service: 'ContractSizeService',
    ) -> None:
        self.__db = db

        # Services
        self.__company_service = company_service
        self.__exchange_service = exchange_service
        self.__ticker_service = ticker_service
        self.__contract_size_service = contract_size_service

        # Cached entities
        self.__exchanges_by_id: Optional[Dict[int, Exchange]] = None
        self.__tickers_by_id: Optional[Dict[int, Ticker]] = None
        self.__companies_by_id: Optional[Dict[int, Company]] = None
        self.__contract_sizes_by_name: Optional[Dict[str, ContractSize]] = None

        self.last_insert_time_by_id: Dict[int, InsertTime] = {}
        self.last_share_hists_by_ticker_id: Dict[int, ShareHist] = {}
        self.last_call_hists_by_id: Dict[int, CallHist] = {}
        self.last_put_hists_by_id: Dict[int, PutHist] = {}

    @property
    def exchanges_by_id(self) -> Dict[int, Exchange]:
        if self.__exchanges_by_id is None:
            with self.__db.connect as conn:
                exchanges = self.__exchange_service.get_all_exchanges(conn)
                self.__exchanges_by_id = {exchange.id: exchange for exchange in exchanges}
        return self.__exchanges_by_id

    @property
    def tickers_by_id(self) -> Dict[int, Ticker]:
        if self.__tickers_by_id is None:
            with self.__db.connect as conn:
                tickers = self.__ticker_service.get_all_tickers(conn)
                self.__tickers_by_id = {ticker.id: ticker for ticker in tickers}
        return self.__tickers_by_id

    @property
    def companies_by_id(self) -> Dict[int, Company]:
        if self.__companies_by_id is None:
            with self.__db.connect as conn:
                companies = self.__company_service.get_all_companies(conn)
                self.__companies_by_id = {exchange.id: exchange for exchange in companies}
        return self.__companies_by_id

    @property
    def contract_sizes_by_name(self) -> Dict[str, ContractSize]:
        if self.__contract_sizes_by_name is None:
            with self.__db.connect as conn:
                contract_sizes = self.__contract_size_service.get_all_contract_sizes(conn)
                self.__contract_sizes_by_name = {contract_size.name: contract_size for contract_size in contract_sizes}
        return self.__contract_sizes_by_name
