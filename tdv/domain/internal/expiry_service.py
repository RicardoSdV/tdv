from datetime import datetime
from typing import List, TYPE_CHECKING, Generator
from sqlalchemy import Connection

from tdv.domain.entities.expiry_entity import Expiry
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.expiry_repo import ExpiryRepo

logger = LoggerFactory.make_logger(__name__)


class ExpiryService:
    def __init__(self, db: 'DB', expiry_repo: 'ExpiryRepo') -> None:
        self.db = db
        self.expiry_repo = expiry_repo

    def get_expiries_with_id(self, expiry_ids: Generator[int, None, None], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_ids=expiry_ids)
        expiries = [Expiry(id=_id) for _id in expiry_ids]
        result = self.expiry_repo.select(conn, expiries)
        return result

    def get_else_create_expiry(self, expiry_date: datetime, ticker_id: int, conn: Connection) -> Expiry:
        selected_expiries = self.__get_expiries_with_date_and_ticker_id(expiry_date, ticker_id, conn)
        if len(selected_expiries) > 0:
            return selected_expiries[0]
        else:
            created_expiries = self.__create_expiry(expiry_date, ticker_id, conn)
            return created_expiries[0]

    def __create_expiry(self, expiry_date: datetime, ticker_id: int, conn: Connection) -> List[Expiry]:
        logger.debug('Creating expiry', expiry_date=expiry_date)
        expiries = [Expiry(ticker_id=ticker_id, date=expiry_date)]
        result = self.expiry_repo.insert(conn, expiries)
        return result

    def __get_expiries_with_date_and_ticker_id(self, date: datetime, ticker_id: int, conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', dates=date, ticker_id=ticker_id)
        expiries = [Expiry(date=date, ticker_id=ticker_id)]
        result = self.expiry_repo.select(conn, expiries)
        return result
