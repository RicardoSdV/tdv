from typing import TYPE_CHECKING, Dict, Optional

from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.domain.entities.call_hist_entity import CallHist
from tdv.domain.entities.exchange_entity import Exchange
from tdv.domain.entities.insert_time_entity import InsertTime
from tdv.domain.entities.put_hist_entity import PutHist
from tdv.domain.entities.share_hist_entity import ShareHist
from tdv.domain.entities.ticker_entity import Ticker

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.internal.company_service import CompanyService
    from tdv.domain.internal.contract_size_service import ContractSizeService
    from tdv.domain.internal.exchange_service import ExchangeService
    from tdv.domain.internal.call_hist_service import CallHistService
    from tdv.domain.internal.put_hist_service import PutHistService
    from tdv.domain.internal.ticker_service import TickerService


class CacheService:
    """For caching entities & more that are used in many places"""

    def __init__(
        self,
        db: 'DB',
        company_service: 'CompanyService',
        exchange_service: 'ExchangeService',
        ticker_service: 'TickerService',
        call_hist_service: 'CallHistService',
        put_hist_service: 'PutHistService',
        contract_size_service: 'ContractSizeService',
    ) -> None:
        self.db = db

        # Services
        self.company_service = company_service
        self.exchange_service = exchange_service
        self.ticker_service = ticker_service
        self.call_hist_service = call_hist_service
        self.put_hist_service = put_hist_service
        self.contract_size_service = contract_size_service

        # Cached entities
        self.__exchanges_by_id: Optional[Dict[int, Exchange]] = None
        self.__tickers_by_id: Optional[Dict[int, Ticker]] = None
        self.__companies_by_id: Optional[Dict[int, Company]] = None
        self.__contract_sizes_by_size: Optional[Dict[int, ContractSize]] = None

        self.last_insert_time_by_ticker_id: Dict[int, InsertTime] = {}
        self.last_share_hists_by_ticker_id: Dict[int, ShareHist] = {}
        self.last_call_hists_by_ticker_id: Dict[int, CallHist] = {}
        self.last_put_hists_by_ticker_id: Dict[int, PutHist] = {}

    @property
    def exchanges_by_id(self) -> Dict[int, Exchange]:
        if self.__exchanges_by_id is None:
            with self.db.connect as conn:
                exchanges = self.exchange_service.get_all_exchanges(conn)
                self.__exchanges_by_id = {exchange.id: exchange for exchange in exchanges}
        return self.__exchanges_by_id

    @property
    def tickers_by_id(self) -> Dict[int, Ticker]:
        if self.__tickers_by_id is None:
            with self.db.connect as conn:
                tickers = self.ticker_service.get_all_tickers(conn)
                self.__tickers_by_id = {ticker.id: ticker for ticker in tickers}
        return self.__tickers_by_id

    @property
    def companies_by_id(self) -> Dict[int, Company]:
        if self.__companies_by_id is None:
            with self.db.connect as conn:
                companies = self.company_service.get_all_companies(conn)
                self.__companies_by_id = {exchange.id: exchange for exchange in companies}
        return self.__companies_by_id

    @property
    def contract_sizes_by_name(self) -> Dict[int, ContractSize]:
        if self.__contract_sizes_by_size is None:
            with self.db.connect as conn:
                contract_sizes = self.contract_size_service.get_all_contract_sizes(conn)
                self.__contract_sizes_by_id = {contract_size.size: contract_size for contract_size in contract_sizes}
        return self.__contract_sizes_by_id
