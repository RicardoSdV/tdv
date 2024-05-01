from typing import Dict

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.expiry_entity import Expiry
from tdv.domain.entities.option_hist_entity import OptionHist
from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.domain.entities.strike_entity import Strike


class Session:
    __slots__ = (
        'id',
        'account',
        'portfolios',
        'portfolio_shares',
        'portfolio_options',
        'strikes',
        'expiries',
        'put_hist',
        'call_hist',
    )

    def __init__(
        self,
        account: Account,
        session_id: int,
        portfolios: Dict[int, Portfolio],
        portfolio_shares: Dict[int, PortfolioShare],
        portfolio_options: Dict[int, PortfolioOption],
        strikes: Dict[int, Strike],
        expiries: Dict[int, Expiry],
        put_hist: Dict[int, OptionHist],
        call_hist: Dict[int, OptionHist],
    ) -> None:
        self.id = session_id
        self.account = account

        # Session specific cached entities
        self.portfolios = portfolios
        self.portfolio_shares = portfolio_shares
        self.portfolio_options = portfolio_options
        self.strikes = strikes
        self.expiries = expiries
        self.put_hist = put_hist
        self.call_hist = call_hist
