from typing import TYPE_CHECKING, Dict

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.domain.entities.call_hist_entity import CallHist
from tdv.domain.entities.put_hist_entity import PutHist
from tdv.domain.entities.ticker_entity import Ticker

from tdv.domain.session.session import Session
from tdv.infra.database import DB

if TYPE_CHECKING:
    from tdv.domain.internal.account_service import AccountService
    from tdv.domain.internal.company_service import CompanyService
    from tdv.domain.internal.contract_size_service import ContractSizeService
    from tdv.domain.internal.exchange_service import ExchangeService
    from tdv.domain.internal.expiry_service import ExpiryService
    from tdv.domain.internal.call_hist_service import CallHistService
    from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
    from tdv.domain.internal.portfolio_service import PortfolioService
    from tdv.domain.internal.portfolio_share_service import PortfolioShareService
    from tdv.domain.internal.put_hist_service import PutHistService
    from tdv.domain.internal.strike_service import StrikeService
    from tdv.domain.internal.ticker_service import TickerService


class SessionManager:
    def __init__(
        self,
        db: DB,
        account_service: 'AccountService',
        company_service: 'CompanyService',
        exchange_service: 'ExchangeService',
        ticker_service: 'TickerService',
        call_hist_service: 'CallHistService',
        put_hist_service: 'PutHistService',
        contract_size_service: 'ContractSizeService',
        pfol_service: 'PortfolioService',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
        strike_service: 'StrikeService',
        expiry_service: 'ExpiryService',
    ) -> None:

        self.sessions: Dict[int, Session] = {}

        # Manager Services
        self.account_service = account_service
        self.company_service = company_service
        self.exchange_service = exchange_service
        self.ticker_service = ticker_service
        self.call_hist_service = call_hist_service
        self.put_hist_service = put_hist_service

        # Session Services
        self.contract_size_service = contract_size_service
        self.pfol_service = pfol_service
        self.pfol_share_service = pfol_share_service
        self.pfol_option_service = pfol_option_service
        self.strike_service = strike_service
        self.expiry_service = expiry_service

        self.db = db

        # Cached entities
        with self.db.connect as conn:
            self.companies: Dict[int, Company] = self.company_service.get_all_companies(conn)
            self.tickers: Dict[int, Ticker] = self.ticker_service.get_all_tickers(conn)
            self.contract_sizes: Dict[int, ContractSize] = self.contact_size_service.get_all_contract_sizes(conn)
            conn.commit()

        self.last_call_hists: Dict[int, CallHist] = self.call_hist_service.get_last_call_hists()
        self.last_put_hists: Dict[int, PutHist] = self.put_hist_service.get_last_call_hists()

    def login(self, username: str, password: str) -> str:
        """
        - Get Account from DB
        - Generate session_id for this account
        - Get all account related data from DB
        - Instantiate session with all the above
        """

        with self.db.connect as conn:
            account = self.account_service.get_or_raise_account_by_username_and_password(username, password, conn)

            session_id = self.__generate_session_id(account)

            portfolios = self.pfol_service.get_portfolios_by_name__with_account_id(account.id, conn)

            portfolio_ids = portfolios.keys()
            pfol_shares_by_id = self.pfol_share_service.get_pfol_shares_by_id(
                portfolio_ids, conn
            )
            portfolio_options = self.pfol_option_service.get_pfol_options_by_id__with_pfol_ids(portfolio_ids, conn)

            strike_ids = [option.strike_id for option in portfolio_options.values()]
            strikes = self.strike_service.get_strikes_by_ids(strike_ids, conn)

            expiry_ids = [strike.expiry_id for strike in strikes.values()]
            expiries = self.expiry_service.get_expiries_by_id(expiry_ids, conn)

            put_hist = self.option_hist_service.get_last_put_hists_by_strike_ids
            call_hist = self.option_hist_service

            session = Session(
                account,
                session_id,
                portfolios,
                portfolio_shares_by_id,
                portfolio_options,
                strikes,
                expiries,
                put_hist,
                call_hist,
            )

        # Get session data

        session = Session(accounts[0])
        self.sessions[session.id] = session
        return session.id

    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)

    def get_session_by_session_id(self, session_id: int) -> Account:
        pass
