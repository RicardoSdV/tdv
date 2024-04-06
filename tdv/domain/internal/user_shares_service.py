from typing import Optional, List

from tdv.domain.entities.user_share_entity import UserShare
from tdv.infra.database import DB
from tdv.infra.repos.user_shares_repo import UserSharesRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class UserSharesService:
    def __init__(self, db: 'DB', user_shares_repo: 'UserSharesRepo') -> None:
        self.db = db
        self.user_shares_repo = user_shares_repo

    def create_user_share(self, user_id: int, ticker_share_type_id: int, count: Optional[int]) -> List[UserShare]:
        logger.debug('Creating user_share', user_id=user_id, ticker_share_type_id=ticker_share_type_id, count=count)
        user_shares = [UserShare(user_id=user_id, ticker_share_type_id=ticker_share_type_id, count=count)]
        with self.db.connect as conn:
            user_shares = self.user_shares_repo.insert(conn, user_shares)
            conn.commit()
        return user_shares
