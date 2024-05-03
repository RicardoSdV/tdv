from typing import TYPE_CHECKING, Dict, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.domain.entities.call_hist_entity import CallHist
from tdv.domain.entities.exchange_entity import Exchange
from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.domain.entities.put_hist_entity import PutHist
from tdv.domain.entities.share_hist_entity import ShareHist
from tdv.domain.entities.ticker_entity import Ticker

from tdv.domain.session.session import Session
from tdv.domain.types import PfolOptionEssentials, IDs

if TYPE_CHECKING:
    from tdv.infra.database import DB
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
            self.exchanges = self.__get_all_exchanges_by_id(conn)
            self.tickers_by_id = self.__get_all_tickers_by_id(conn)
            self.companies = self.__get_all_companies_by_id(conn)
            self.contract_sizes = self.__get_all_contract_sizes_by_id(conn)

            self.last_share_hists_by_id: Dict[int, ShareHist] = {}
            self.last_call_hists_by_id: Dict[int, CallHist] = {}
            self.last_put_hists_by_id: Dict[int, PutHist] = {}

            conn.commit()

    def login(self, name: str, password: str) -> Session:
        """
        - Get Account from DB
        - Generate session_id for this account
        - Get all account related data from DB
        - Instantiate session with all the above
        - Update self.sessions with the new session
        """

        # TODO: Check that the account is not already logged in
        # TODO: Validate password

        with self.db.connect as conn:

            account = self.account_service.get_or_raise_account_with_name(name, conn)

            session_id = self.__generate_session_id(account)

            pfols_by_name, pfol_ids = self.__get_pfols_by_name_and_pfol_ids(account.id, conn)

            pfol_shares_by_ticker, pfol_share_ids = self.__get_pfol_shares_and_ids(pfol_ids, conn)
            pfol_option_essentials = self.__get_pfol_options_expiries_and_strikes(pfol_ids, conn)
            pfol_options_by_ticker, strikes_by_id, expiries_by_id = pfol_option_essentials

            session = Session(
                account=account,
                session_id=session_id,
                pfols_by_name=pfols_by_name,
                pfol_shares_by_ticker=pfol_shares_by_ticker,
                pfol_options_by_ticker=pfol_options_by_ticker,
                strikes_by_id=strikes_by_id,
                expiries_by_id=expiries_by_id,
            )

        self.sessions[session.id] = session
        return session

    """ Getting shared Entities """

    def __get_all_exchanges_by_id(self, conn: Connection) -> Dict[int, Exchange]:
        exchanges = self.exchange_service.get_all_exchanges(conn)
        exchanges_by_id = {exchange.id: exchange for exchange in exchanges}
        return exchanges_by_id

    def __get_all_tickers_by_id(self, conn: Connection) -> Dict[int, Ticker]:
        tickers = self.ticker_service.get_all_tickers(conn)
        tickers_by_id = {ticker.id: ticker for ticker in tickers}
        return tickers_by_id

    def __get_all_companies_by_id(self, conn: Connection) -> Dict[int, Company]:
        companies = self.company_service.get_all_companies(conn)
        companies_by_id = {exchange.id: exchange for exchange in companies}
        return companies_by_id

    def __get_all_contract_sizes_by_id(self, conn: Connection) -> Dict[int:ContractSize]:
        contract_sizes = self.contract_size_service.get_all_contract_sizes(conn)
        contract_sizes_by_id = {contract_size.id: contract_size for contract_size in contract_sizes}
        return contract_sizes_by_id

    """ Getting session Entities """

    def __get_pfols_by_name_and_pfol_ids(self, account_id: int, conn: Connection) -> Tuple[Dict[str, Portfolio], IDs]:
        portfolios = self.portfolio_service.get_portfolios_with_account_id(account_id, conn)
        pfols_by_name = {pfol.name: pfol for pfol in portfolios if pfol.name is not None}
        pfol_ids = [pfol.id for pfol in portfolios if pfol.id is not None]
        return pfols_by_name, pfol_ids

    def __get_pfol_shares_and_ids(self, pfol_ids: IDs, conn: Connection) -> Dict[str, PortfolioShare]:
        portfolio_shares = self.pfol_share_service.get_portfolio_shares(pfol_ids, conn)

        pfol_shares_by_ticker = {}
        for pfol_share in portfolio_shares:
            ticker_id = pfol_share.ticker_id
            ticker = self.tickers_by_id[ticker_id]
            pfol_shares_by_ticker[ticker.name] = pfol_share

        return pfol_shares_by_ticker

    def __get_pfol_options_expiries_and_strikes(self, pfol_ids: IDs, conn: Connection) -> PfolOptionEssentials:
        portfolio_options = self.pfol_option_service.get_portfolio_options(pfol_ids, conn)

        strikes = self.strike_service.get_strikes((pfol_option.strike_id for pfol_option in portfolio_options), conn)
        expiries = self.expiry_service.get_expiries((strike.expiry_id for strike in strikes), conn)

        pfol_options_by_ticker = {}
        for pfol_option, expiry in zip(portfolio_options, expiries):
            ticker_id = expiry.ticker_id
            ticker = self.tickers_by_id[ticker_id]
            pfol_options_by_ticker[ticker.name] = pfol_option

        strikes_by_id = {strike.id: strike for strike in strikes}
        expiries_by_id = {expiry.id: expiry for expiry in expiries}

        return pfol_options_by_ticker, strikes_by_id, expiries_by_id

    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)

    def get_session_by_session_id(self, session_id: int) -> Account:
        pass
