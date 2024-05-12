from typing import TYPE_CHECKING, Dict, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.independent_entities.account_entity import Account
from tdv.domain.entities.option_entities.expiry_entity import Expiry
from tdv.domain.entities.option_entities.strike_entity import Strike
from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_entities.portfolio_share_entity import PortfolioShare
from tdv.domain.session.session import Session
from tdv.domain.types import IDs, TickerName, StrikeID, ExpiryID
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.domain.services.independent_services.account_service import AccountService
    from tdv.domain.services.option_services.expiry_service import ExpiryService
    from tdv.domain.services.option_services.strike_service import StrikeService
    from tdv.domain.services.portfolio_services.portfolio_option_service import PortfolioOptionService
    from tdv.domain.services.portfolio_services.portfolio_service import PortfolioService
    from tdv.domain.services.portfolio_services.portfolio_share_service import PortfolioShareService

logger = LoggerFactory.make_logger(__name__)

PfolsByName = Dict[str, Portfolio]
PfolSharesByTickerName = Dict[str, PortfolioShare]

PfolOptionsByTickerName = Dict[TickerName, PortfolioOption]
StrikeByID = Dict[StrikeID, Strike]
ExpiryByID = Dict[ExpiryID, Expiry]
PfolOptionEssentials = Tuple[PfolOptionsByTickerName, StrikeByID, ExpiryByID]

AccountAndData = Tuple[Account, PfolsByName, PfolSharesByTickerName, PfolOptionEssentials]


class SessionManager:
    def __init__(
        self,
        db: 'DB',
        entity_cache: 'EntityCache',
        account_service: 'AccountService',
        portfolio_service: 'PortfolioService',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
        strike_service: 'StrikeService',
        expiry_service: 'ExpiryService',
    ) -> None:

        self.sessions_by_id: Dict[int, Session] = {}

        self.__db = db
        self.__entity_cache = entity_cache
        self.__account_service = account_service
        self.__portfolio_service = portfolio_service
        self.__pfol_share_service = pfol_share_service
        self.__pfol_option_service = pfol_option_service
        self.__strike_service = strike_service
        self.__expiry_service = expiry_service

    def login(self, account_name: str, password: str) -> Session:
        """
        - Get Session & Generate session_id for this account
        - Update self.sessions with the new session
        """
        logger.debug('Login', account_name=account_name, password=password)
        # TODO: Check that the account is not already logged in & Validate password

        with self.__db.connect as conn:
            session = self.__get_session(account_name, conn)

        session.id = self.__generate_session_id(session.account)
        self.sessions_by_id[session.id] = session

        return session

    def logout(self, session_id: int) -> None:
        """
        - Get Session with the new data from self.sessions_by_id
        - Get Session with the old data from DB
        - Compare old & new session data
        - Insert/Update/Delete from be DB based on the comparison
        """
        logger.debug('Logout', session_id=session_id)
        new_session = self.sessions_by_id[session_id]

        with self.__db.connect as conn:
            old_session = self.__get_session(new_session.account.name, conn)

            self.__compare_accounts_db_diff(old_session.account, new_session.account, conn)
            self.__compare_portfolios_db_diff(old_session.portfolios_by_name, new_session.portfolios_by_name, conn)

    def __compare_accounts_db_diff(self, old_account: Account, new_account: Account, conn: Connection) -> None:
        pass

    def __compare_portfolios_db_diff(
        self, old_portfolio: PfolsByName, new_portfolio: PfolsByName, conn: Connection
    ) -> None:
        pass

    def __get_session(self, account_name: str, conn: Connection) -> Session:
        """
        - Get Account from DB
        - Get all account related data from DB
        - Return session with all the above
        """
        account = self.__account_service.get_or_raise_account_with_name(account_name, conn)

        pfols_by_name, pfol_ids = self.__get_pfols_by_name_and_pfol_ids(account.id, conn)
        pfol_shares_by_ticker = self.__get_pfol_shares_by_ticker_name(pfol_ids, conn)
        pfol_option_essentials = self.__get_pfol_options_expiries_and_strikes(pfol_ids, conn)

        pfol_options_by_ticker, strikes_by_id, expiries_by_id = pfol_option_essentials

        return Session(
            id=-1,
            account=account,
            portfolios_by_name=pfols_by_name,
            portfolios_shares_by_ticker=pfol_shares_by_ticker,
            portfolios_options_by_ticker=pfol_options_by_ticker,
            strikes_by_id=strikes_by_id,
            expiries_by_id=expiries_by_id,
        )

    def __get_account_and_related_data(self, account_name: str, conn: Connection) -> AccountAndData:
        account = self.__account_service.get_or_raise_account_with_name(account_name, conn)

        pfols_by_name, pfol_ids = self.__get_pfols_by_name_and_pfol_ids(account.id, conn)
        pfol_shares_by_ticker = self.__get_pfol_shares_by_ticker_name(pfol_ids, conn)
        pfol_option_essentials = self.__get_pfol_options_expiries_and_strikes(pfol_ids, conn)

        return account, pfols_by_name, pfol_shares_by_ticker, pfol_option_essentials

    def __get_pfols_by_name_and_pfol_ids(self, account_id: int, conn: Connection) -> Tuple[Dict[str, Portfolio], IDs]:
        portfolios = self.__portfolio_service.get_portfolios_with_account_id(account_id, conn)
        pfols_by_name = {pfol.name: pfol for pfol in portfolios if pfol.name is not None}
        pfol_ids = [pfol.id for pfol in portfolios if pfol.id is not None]
        return pfols_by_name, pfol_ids

    def __get_pfol_shares_by_ticker_name(self, pfol_ids: IDs, conn: Connection) -> Dict[str, PortfolioShare]:
        portfolio_shares = self.__pfol_share_service.get_portfolio_shares(pfol_ids, conn)

        pfol_shares_by_ticker = {}
        for pfol_share in portfolio_shares:
            ticker_id = pfol_share.ticker_id
            ticker = self.__entity_cache.tickers_by_id[ticker_id]
            pfol_shares_by_ticker[ticker.name] = pfol_share

        return pfol_shares_by_ticker

    def __get_pfol_options_expiries_and_strikes(self, pfol_ids: IDs, conn: Connection) -> PfolOptionEssentials:
        portfolio_options = self.__pfol_option_service.get_portfolio_options(pfol_ids, conn)

        strikes = self.__strike_service.get_strikes_with_ids(
            (pfol_option.strike_id for pfol_option in portfolio_options), conn
        )
        expiries = self.__expiry_service.get_expiries_with_id((strike.expiry_id for strike in strikes), conn)

        pfol_options_by_ticker = {}
        for pfol_option, expiry in zip(portfolio_options, expiries):
            ticker_id = expiry.ticker_id
            ticker = self.__entity_cache.tickers_by_id[ticker_id]
            pfol_options_by_ticker[ticker.name] = pfol_option

        strikes_by_id = {strike.id: strike for strike in strikes}
        expiries_by_id = {expiry.id: expiry for expiry in expiries}

        return pfol_options_by_ticker, strikes_by_id, expiries_by_id

    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)
