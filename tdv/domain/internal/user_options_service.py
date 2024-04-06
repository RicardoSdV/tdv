from typing import List, Optional

from tdv.domain.entities.user_options_entity import UserOption
from tdv.infra.database import DB
from tdv.infra.repos.user_options_repo import UserOptionsRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


# TODO: change counts from floats to Decimal
class UserOptionsService:
    def __init__(self, db: 'DB', user_options_repo: 'UserOptionsRepo') -> None:
        self.db = db
        self.user_options_repo = user_options_repo

    def create_user_options(self, user_id: int, option_id: int, count: Optional[float]) -> List[UserOption]:
        logger.debug('Creating user_options', user_id=user_id, option_id=option_id, count=count)
        user_options = [UserOption(user_id=user_id, option_id=option_id, count=count)]

        with self.db.connect as conn:
            result = self.user_options_repo.insert(conn, user_options)
            conn.commit()
        return result
