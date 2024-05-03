from typing import Dict

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.base_entity import Entity
from tdv.domain.entities.expiry_entity import Expiry
from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.domain.entities.strike_entity import Strike


class Session(Entity):  # TODO: Find a better way, Session is not an Entity
    __slots__ = (
        'id',
        'account',
        'pfols_by_name',
        'pfol_shares_by_ticker',
        'pfol_options_by_ticker',
        'strikes_by_id',
        'expiries_by_id',
    )

    def __init__(
        self,
        account: Account,
        session_id: int,
        pfols_by_name: Dict[str, Portfolio],
        pfol_shares_by_ticker: Dict[str, PortfolioShare],
        pfol_options_by_ticker: Dict[str, PortfolioOption],
        strikes_by_id: Dict[int, Strike],
        expiries_by_id: Dict[int, Expiry],
    ) -> None:
        self.id = session_id
        self.account = account

        # Session specific cached entities
        self.pfols_by_name = pfols_by_name
        self.pfol_shares_by_ticker = pfol_shares_by_ticker
        self.pfol_options_by_ticker = pfol_options_by_ticker
        self.strikes_by_id = strikes_by_id
        self.expiries_by_id = expiries_by_id
