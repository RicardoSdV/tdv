from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Connection

from tdv.domain.entities.insert_time_entity import InsertTime

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.insert_time_repo import InsertTimeRepo


logger = LoggerFactory.make_logger(__name__)


class InsertTimeService:
    def __init__(self, db: 'DB', insert_time_repo: 'InsertTimeRepo') -> None:
        self.db = db
        self.insert_time_repo = insert_time_repo

    def create_insert_time(self, conn: Connection) -> InsertTime:
        insert_time = InsertTime(time=datetime.now())
        logger.debug('Creating InsertTime', insert_time=insert_time)
        insert_times = self.insert_time_repo.insert(conn, [insert_time])
        assert len(insert_times) == 1
        return insert_times[0]
