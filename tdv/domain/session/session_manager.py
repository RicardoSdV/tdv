from typing import TYPE_CHECKING, Dict, List, Iterable, Optional, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.base_entity import Entity
from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.domain.entities.call_hist_entity import CallHist
from tdv.domain.entities.exchange_entity import Exchange
from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.domain.entities.put_hist_entity import PutHist
from tdv.domain.entities.share_hist_entity import ShareHist
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
        portfolio_service: 'PortfolioService',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
        strike_service: 'StrikeService',
        expiry_service: 'ExpiryService',
    ) -> None:

        self.sessions: Dict[int, Session] = {}

        self.db = db

        # Manager Services
        self.account_service = account_service
        self.company_service = company_service
        self.exchange_service = exchange_service
        self.ticker_service = ticker_service
        self.call_hist_service = call_hist_service
        self.put_hist_service = put_hist_service

        # Session Services
        self.contract_size_service = contract_size_service
        self.portfolio_service = portfolio_service
        self.pfol_share_service = pfol_share_service
        self.pfol_option_service = pfol_option_service
        self.strike_service = strike_service
        self.expiry_service = expiry_service

        with db.connect as conn:

            # Shared cached entities, those used by all sessions
            self.exchanges: Dict[str, Exchange] = {}
            self.tickers_by_name, self.tickers_by_id = self.__get_all_tickers_by_name_and_id(conn)
            self.companies: Dict[int, Company] = {}
            self.last_share_hists: Dict[int, ShareHist] = {}
            self.last_call_hists: Dict[int, CallHist] = {}
            self.last_put_hists: Dict[int, PutHist] = {}
            self.contract_sizes: Dict[int, ContractSize] = {}

            conn.commit()


    def login(self, name: str, password: str) -> Optional[int]:
        """
        - Get Account from DB
        - Generate session_id for this account
        - Get all account related data from DB
        - Instantiate session with all the above
        """

        with self.db.connect as conn:

            account = self.account_service.get_or_raise_account_with_name(name, conn)

            session_id = self.__generate_session_id(account)

            pfols_by_name, pfol_ids = self.__get_pfols_by_name_and_pfol_ids(account.id, conn)

            pfol_shares_by_ticker, pfol_share_ids = self.__get_pfol_shares_and_ids(pfol_ids, conn)
            pfol_options_by_ticker, pfol_option_ids = self.__get_pfol_options_and_ids(pfol_ids, conn)

            strike_ids = [option.strike_id for option in portfolio_options.values()]
            strikes = self.strike_service.get_strikes_by_ids(strike_ids, conn)

            expiry_ids = [strike.expiry_id for strike in strikes.values()]
            expiries = self.expiry_service.get_expiries_by_id(expiry_ids, conn)

            put_hist = self.option_hist_service.get_last_put_hists_by_strike_ids
            call_hist = self.option_hist_service

            session = Session(
                account,
                session_id,
                pfols_by_name,
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

    def __get_all_tickers_by_name_and_id(self, conn: Connection) -> Tuple[Dict[str, Ticker], Dict[int, Ticker]]:
        tickers = self.ticker_service.get_all_tickers(conn)
        tickers_by_name = {ticker.name: ticker for ticker in tickers}
        tickers_by_id = {ticker.id: ticker for ticker in tickers}
        return tickers_by_name, tickers_by_id


    def __get_pfols_by_name_and_pfol_ids(self, account_id: int, conn: Connection) -> Tuple[Dict[str, Portfolio], List[int]]:
        portfolios = self.portfolio_service.get_portfolios_with_account_id(account_id, conn)
        pfols_by_name = {pfol.name: pfol for pfol in portfolios if pfol.name is not None}
        pfol_ids = [pfol.id for pfol in portfolios if pfol.id is not None]
        return pfols_by_name, pfol_ids

    def __get_pfol_shares_and_ids(self, pfol_ids: List[int], conn: Connection) -> Tuple[Dict[str, PortfolioShare], List[int]]:
        portfolio_shares = self.pfol_share_service.get_portfolio_shares(pfol_ids, conn)

        pfol_shares_by_ticker = {'placeholder':}

    def __get_pfol_options_and_ids(self, pfol_ids: List[int], conn: Connection) -> Tuple[Dict[str, PortfolioOption], List[int]]:
        portfolio_options = self.pfol_option_service.get_portfolio_options(pfol_ids, conn)




    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)

    @staticmethod
    def __get_entities_ids(entities: Iterable[Entity]) -> List[int]:
        pass

    def get_session_by_session_id(self, session_id: int) -> Account:
        pass
