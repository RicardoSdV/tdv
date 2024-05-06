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

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.services_internal.cache_service import CacheService
    from tdv.domain.services_internal.independent_services.account_service import AccountService
    from tdv.domain.services_internal.option_services.expiry_service import ExpiryService
    from tdv.domain.services_internal.option_services.strike_service import StrikeService
    from tdv.domain.services_internal.portfolio_services.portfolio_option_service import PortfolioOptionService
    from tdv.domain.services_internal.portfolio_services.portfolio_service import PortfolioService
    from tdv.domain.services_internal.portfolio_services.portfolio_share_service import PortfolioShareService


PfolOptionsByTickerName = Dict[TickerName, PortfolioOption]
StrikeByID = Dict[StrikeID, Strike]
ExpiryByID = Dict[ExpiryID, Expiry]
PfolOptionEssentials = Tuple[PfolOptionsByTickerName, StrikeByID, ExpiryByID]


class SessionManager:
    def __init__(
        self,
        db: 'DB',
        cache_service: 'CacheService',
        account_service: 'AccountService',
        portfolio_service: 'PortfolioService',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
        strike_service: 'StrikeService',
        expiry_service: 'ExpiryService',
    ) -> None:

        self.sessions: Dict[int, Session] = {}

        self.__db = db
        self.__cache_service = cache_service
        self.__account_service = account_service
        self.__portfolio_service = portfolio_service
        self.__pfol_share_service = pfol_share_service
        self.__pfol_option_service = pfol_option_service
        self.__strike_service = strike_service
        self.__expiry_service = expiry_service

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

        with self.__db.connect as conn:
            account = self.__account_service.get_or_raise_account_with_name(name, conn)

            session_id = self.__generate_session_id(account)

            pfols_by_name, pfol_ids = self.__get_pfols_by_name_and_pfol_ids(account.id, conn)

            pfol_shares_by_ticker, pfol_share_ids = self.__get_pfol_shares_and_ids(pfol_ids, conn)
            pfol_option_essentials = self.__get_pfol_options_expiries_and_strikes(pfol_ids, conn)
            pfol_options_by_ticker, strikes_by_id, expiries_by_id = pfol_option_essentials

            session = Session(
                id=session_id,
                account=account,
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
        portfolios = self.__portfolio_service.get_portfolios_with_account_id(account_id, conn)
        pfols_by_name = {pfol.name: pfol for pfol in portfolios if pfol.name is not None}
        pfol_ids = [pfol.id for pfol in portfolios if pfol.id is not None]
        return pfols_by_name, pfol_ids

    def __get_pfol_shares_and_ids(self, pfol_ids: IDs, conn: Connection) -> Dict[str, PortfolioShare]:
        portfolio_shares = self.__pfol_share_service.get_portfolio_shares(pfol_ids, conn)

        pfol_shares_by_ticker = {}
        for pfol_share in portfolio_shares:
            ticker_id = pfol_share.ticker_id
            ticker = self.__cache_service.tickers_by_id[ticker_id]
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
            ticker = self.__cache_service.tickers_by_id[ticker_id]
            pfol_options_by_ticker[ticker.name] = pfol_option

        strikes_by_id = {strike.id: strike for strike in strikes}
        expiries_by_id = {expiry.id: expiry for expiry in expiries}

        return pfol_options_by_ticker, strikes_by_id, expiries_by_id

    @staticmethod
    def __generate_session_id(account: Account) -> int:
        return hash(account.id)

    def get_session_by_session_id(self, session_id: int) -> Account:
        pass
