from typing import TYPE_CHECKING, Dict

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.domain.entities.ticker_entity import Ticker
from tdv.domain.session.session import Session

if TYPE_CHECKING:
    from tdv.domain.internal.account_service import AccountService
    from tdv.domain.internal.company_service import CompanyService
    from tdv.domain.internal.contract_size_service import ContractSizeService
    from tdv.domain.internal.exchange_service import ExchangeService
    from tdv.domain.internal.expiry_service import ExpiryService
    from tdv.domain.internal.option_hist_service import OptionHistService
    from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
    from tdv.domain.internal.portfolio_service import PortfolioService
    from tdv.domain.internal.portfolio_share_service import PortfolioShareService
    from tdv.domain.internal.strike_service import StrikeService
    from tdv.domain.internal.ticker_service import TickerService


class SessionManager:
    def __init__(
        self,
        account_service: 'AccountService',
        company_service: 'CompanyService',
        exchange_service: 'ExchangeService',
        ticker_service: 'TickerService',
        contract_size_service: 'ContractSizeService',
        portfolio_service: 'PortfolioService',
        portfolio_share_service: 'PortfolioShareService',
        portfolio_option_service: 'PortfolioOptionService',
        strike_service: 'StrikeService',
        expiry_service: 'ExpiryService',
        option_hist_service: 'OptionHistService',
    ) -> None:

        self.sessions: Dict[int, Session] = {}

        # Services
        self.account_service = account_service
        self.company_service = company_service
        self.exchange_service = exchange_service
        self.ticker_service = ticker_service
        self.contract_size_service = contract_size_service
        self.portfolio_service = portfolio_service
        self.portfolio_share_service = portfolio_share_service
        self.portfolio_option_service = portfolio_option_service
        self.strike_service = strike_service
        self.expiry_service = expiry_service
        self.option_hist_service = option_hist_service

        # Cached entities
        self.companies: Dict[int, Company] = {}
        self.tickers: Dict[int, Ticker] = {}
        self.contract_sizes: Dict[int, ContractSize] = {}

    def login(self, username: str, password: str) -> str:

        """
        - Get Account from DB
        - Create session and session_id for this account
        - Get all account related data
        -
        """

        accounts = self.account_service.get_account_by_username_and_password(username, password)
        assert len(accounts) == 1
        session = Session(accounts[0])
        self.sessions[session.id] = session
        return session.id

    def get_account_by_session_id(self, session_id: str) -> Account:
        pass
