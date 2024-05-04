from typing import TYPE_CHECKING, Dict, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.account_entity import Account
from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_share_entity import PortfolioShare

from tdv.domain.session.session import Session
from tdv.domain.types import PfolOptionEssentials, IDs

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.internal.account_service import AccountService
    from tdv.domain.internal.cache_service import CacheService
    from tdv.domain.internal.expiry_service import ExpiryService
    from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
    from tdv.domain.internal.portfolio_service import PortfolioService
    from tdv.domain.internal.portfolio_share_service import PortfolioShareService
    from tdv.domain.internal.strike_service import StrikeService


class SessionManager:
    def __init__(
            self,
            db: DB,
            cache_service: 'CacheService',
            account_service: 'AccountService',
            portfolio_service: 'PortfolioService',
            pfol_share_service: 'PortfolioShareService',
            pfol_option_service: 'PortfolioOptionService',
            strike_service: 'StrikeService',
            expiry_service: 'ExpiryService',
    ) -> None:

        self.db = db
        self.sessions: Dict[int, Session] = {}
        self.cache_service = cache_service
        self.account_service = account_service
        self.portfolio_service = portfolio_service
        self.pfol_share_service = pfol_share_service
        self.pfol_option_service = pfol_option_service
        self.strike_service = strike_service
        self.expiry_service = expiry_service

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
            ticker = self.cache_service.tickers_by_id[ticker_id]
            pfol_shares_by_ticker[ticker.name] = pfol_share

        return pfol_shares_by_ticker

    def __get_pfol_options_expiries_and_strikes(self, pfol_ids: IDs, conn: Connection) -> PfolOptionEssentials:
        portfolio_options = self.pfol_option_service.get_portfolio_options(pfol_ids, conn)

        strikes = self.strike_service.get_strikes((pfol_option.strike_id for pfol_option in portfolio_options), conn)
        expiries = self.expiry_service.get_expiries_with_id((strike.expiry_id for strike in strikes), conn)

        pfol_options_by_ticker = {}
        for pfol_option, expiry in zip(portfolio_options, expiries):
            ticker_id = expiry.ticker_id
            ticker = self.cache_service.tickers_by_id[ticker_id]
            pfol_options_by_ticker[ticker.name] = pfol_option

        strikes_by_id = {strike.id: strike for strike in strikes}
        expiries_by_id = {expiry.id: expiry for expiry in expiries}

        return pfol_options_by_ticker, strikes_by_id, expiries_by_id

    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)

    def get_session_by_session_id(self, session_id: int) -> Account:
        pass
