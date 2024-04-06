from typing import Optional, List

from tdv.domain.entities.user_share_entity import UserShare
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.infra.database import DB
from tdv.infra.repos.user_shares_repo import UserSharesRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class UserSharesService:
    def __init__(
            self,
            db: 'DB',
            user_shares_repo: 'UserSharesRepo',
            ticker_service: 'TickerService',
            share_type_service: 'ShareTypeService',
    ) -> None:
        self.db = db
        self.user_shares_repo = user_shares_repo
        self.ticker_service = ticker_service
        self.share_type_service = share_type_service

    def create_user_shares(self, user_id: int, ticker_share_type_id: int, count: Optional[float]) -> List[UserShare]:
        logger.debug('Creating user_shares', user_id=user_id, ticker_share_type_id=ticker_share_type_id, count=count)
        user_shares = [UserShare(user_id=user_id, ticker_share_type_id=ticker_share_type_id, count=count)]
        with self.db.connect as conn:
            result = self.user_shares_repo.insert(conn, user_shares)
            conn.commit()
        return result

    def delete_user_shares_by_id(self, user_shares_id: int) -> List[UserShare]:
        logger.debug('Deleting user_shares', user_shares_id=user_shares_id)
        user_shares = [UserShare(user_share_id=user_shares_id)]
        with self.db.connect as conn:
            result = self.user_shares_repo.delete(conn, user_shares)
            conn.commit()
        return result

    def update_count_by_user_id_and_share_type(self, user_id: int, ticker: str, share_type: str, count: float) -> List[UserShare]:
        logger.debug('Updating user_shares count', user_id=user_id, ticker=ticker, share_type=share_type, new_count=count)
        params = {'count': count}
        with self.db.connect as conn:
            tickers = self.ticker_service.get_ticker_by_name(ticker, conn)
            ticker_id = tickers[0].id
            assert isinstance(ticker_id, int)
            ticker_share_types = self.share_type_service.get_ticker_share_type_by_ticker_id(ticker_id, conn)
            ticker_share_type_id = ticker_share_types[0].id
            user_shares = [UserShare(user_id=user_id, ticker_share_type_id=ticker_share_type_id)]
            result = self.user_shares_repo.update(conn, user_shares, params)
            conn.commit()
        return result
