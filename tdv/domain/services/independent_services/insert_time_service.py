from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Connection

from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.independent_repos.insert_time_repo import InsertTimeRepo


logger = LoggerFactory.make_logger(__name__)


class InsertTimeService:
    def __init__(self, insert_time_repo: 'InsertTimeRepo') -> None:
        self.__insert_time_repo = insert_time_repo

    def create_insert_time__utcnow(self, conn: Connection) -> InsertTime:
        insert_time = InsertTime(time=datetime.utcnow())
        logger.debug('Creating InsertTime', insert_time=insert_time)
        insert_times = self.__insert_time_repo.insert(conn, [insert_time])
        assert len(insert_times) == 1
        return insert_times[0]
