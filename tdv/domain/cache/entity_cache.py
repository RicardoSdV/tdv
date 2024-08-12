from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    from tdv.domain.entities.independent_entities.company_entity import Company
    from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
    from tdv.domain.entities.independent_entities.exchange_entity import Exchange
    from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
    from tdv.domain.entities.option_entities.call_hist_entity import CallHist
    from tdv.domain.entities.option_entities.put_hist_entity import PutHist
    from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist
    from tdv.domain.entities.ticker_entities.ticker_entity import Ticker


class EntityCache:
    """Wrapper for entities indexed by relevant attrs"""

    def __init__(self) -> None:

        self.exchanges_by_id       : 'Optional[Dict[int, Exchange]]'     = None
        self.tickers_by_id         : 'Optional[Dict[int, Ticker]]'      = None
        self.tickers_by_name       : 'Optional[Dict[str, Ticker]]'      = None
        self.companies_by_id       : 'Optional[Dict[int, Company]]'      = None
        self.contract_sizes_by_name: 'Optional[Dict[str, ContractSize]]' = None

        self.last_insert_time_by_id       : 'Optional[Dict[int, InsertTime]]' = None
        self.last_share_hists_by_ticker_id: 'Optional[Dict[int, ShareHist]]'  = None
        self.last_call_hists_by_id        : 'Optional[Dict[int, CallHist]]'   = None
        self.last_put_hists_by_id         : 'Optional[Dict[int, PutHist]]'    = None

    @property
    def exchanges(self) -> 'ValuesView[Exchange]':
        return self.exchanges_by_id.values()

    @property
    def exchange_names(self) -> 'Iterator[str]':
        return (exchange.name for exchange in self.exchanges)

    @property
    def tickers(self) -> 'ValuesView[Ticker]':
        return self.tickers_by_id.values()

    @property
    def companies(self) -> 'ValuesView[Company]':
        return self.companies_by_id.values()

    @property
    def contract_sizes(self) -> 'ValuesView[ContractSize]':
        return self.contract_sizes_by_name.values()

    def cache_exchanges(self, exchanges: List[Exchange]) -> None:
        self.exchanges_by_id = {exchange.id: exchange for exchange in exchanges}

    def cache_tickers(self, tickers: List[Ticker]) -> None:
        self.tickers_by_id = {ticker.id: ticker for ticker in tickers}
        self.tickers_by_name = {ticker.name: ticker for ticker in tickers}

    def cache_companies(self, companies: List[Company]) -> None:
        self.companies_by_id = {company.id: company for company in companies}

    def cache_contract_sizes(self, contract_sizes: List[ContractSize]) -> None:
        self.contract_sizes_by_name = {contract_size.name: contract_size for contract_size in contract_sizes}
