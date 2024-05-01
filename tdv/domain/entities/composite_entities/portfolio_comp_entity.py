from typing import List

from tdv.domain.entities.atomic_entities.company_entity import Company
from tdv.domain.entities.atomic_entities.contract_size_entity import ContractSize
from tdv.domain.entities.atomic_entities.exchange_entity import Exchange
from tdv.domain.entities.atomic_entities.expiry_entity import Expiry
from tdv.domain.entities.atomic_entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.atomic_entities.portfolio_share_entity import PortfolioShare
from tdv.domain.entities.atomic_entities.share_hist_entity import ShareHist
from tdv.domain.entities.atomic_entities.strike_entity import Strike
from tdv.domain.entities.atomic_entities.ticker_entity import Ticker

PortfolioShare
PortfolioOption
Strike
Expiry
ContractSize
Ticker
Exchange
Company
ShareHist






class ShareComp:
    def __init__(self) -> None:
        self.ticker = None


class OptionComposite:
    def __init__(self) -> None:
        self.portfolio_option = None
        self.strike = None
        self.expiry = None
        self.contract_size = None
        self.ticker = None
        self.company = None


class PortfolioComposite:
    def __init__(self) -> None:
        self.portfolio = None
        self.share_composites: List[ShareComp] = []
        self.option_composites: List[OptionComposite] = []
