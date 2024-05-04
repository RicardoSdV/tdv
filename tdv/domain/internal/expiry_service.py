from datetime import datetime
from typing import List, TYPE_CHECKING, Iterator, Iterable

from sqlalchemy import Connection

from tdv.domain.entities.expiry_entity import Expiry
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.expiry_repo import ExpiryRepo

logger = LoggerFactory.make_logger(__name__)


class ExpiryService:
    def __init__(self, db: DB, expiry_repo: ExpiryRepo) -> None:
        self.db = db
        self.expiry_repo = expiry_repo

    def get_expiries_with_id(self, expiry_ids: Iterator[int], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_ids=expiry_ids)
        expiries = [Expiry(expiry_id=_id) for _id in expiry_ids]
        result = self.expiry_repo.select(conn, expiries)
        return result

    def get_expiries_with_date(self, expiry_dates: Iterable[str], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_dates=expiry_dates)
        expiries = [Expiry(expiry_date=self.__str_to_datetime(date)) for date in expiry_dates]
        result = self.expiry_repo.select(conn, expiries)
        return result

    def get_else_create_many_expiries(self, expiry_dates: Iterable[str], ticker_id: int, conn: Connection) -> List[Expiry]:
        """
        Case 1 - Expiries dont exist in DB, they are inserted
        Case 2 - Expiries exist in DB, they are selected
        Case 3 - Some expiries exist in DB, some dont, those that exist are created those that dont are inserted
        """

        expiries = self.


    def __create_many_expiries(self, expiry_dates: Iterable[str], ticker_id: int, conn: Connection) -> List[Expiry]:
        logger.debug('Creating expiries', expiry_dates=expiry_dates)
        expiries = [Expiry(ticker_id=ticker_id, expiry_date=self.__str_to_datetime(date)) for date in expiry_dates]
        result = self.expiry_repo.insert(conn, expiries)
        return result

    @staticmethod
    def __str_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string, '%Y-%m-%d')
