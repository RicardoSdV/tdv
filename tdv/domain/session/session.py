from dataclasses import dataclass
from typing import Dict

from tdv.domain.entities.independent_entities.account_entity import Account
from tdv.domain.entities.option_entities.expiry_entity import Expiry
from tdv.domain.entities.option_entities.strike_entity import Strike
from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_entities.portfolio_share_entity import PortfolioShare


@dataclass(slots=True)
class Session:
    account: Account
    session_id: int
    pfols_by_name: Dict[str, Portfolio]
    pfol_shares_by_ticker: Dict[str, PortfolioShare]
    pfol_options_by_ticker: Dict[str, PortfolioOption]
    strikes_by_id: Dict[int, Strike]
    expiries_by_id: Dict[int, Expiry]
