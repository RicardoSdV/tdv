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
    def __init__(self, db: 'DB', expiry_repo: 'ExpiryRepo') -> None:
        self.db = db
        self.expiry_repo = expiry_repo

    def get_expiries_with_id(self, expiry_ids: Iterator[int], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_ids=expiry_ids)
        expiries = [Expiry(expiry_id=_id) for _id in expiry_ids]
        result = self.expiry_repo.select(conn, expiries)
        return result

    def get_else_create_expiries(
        self, expiry_date_strs: Iterable[str], ticker_id: int, contract_size_id: int, conn: Connection
    ) -> List[Expiry]:
        expiry_dates = [self.__str_to_datetime(date) for date in expiry_date_strs]

        selected_expiries = self.__get_expiries_with_date(expiry_dates, conn)
        selected_dates = [expiry.date for expiry in selected_expiries]

        missing_dates = list(set(expiry_dates) - set(selected_dates))
        created_expiries = self.__create_many_expiries(missing_dates, ticker_id, contract_size_id, conn)

        logger.debug(
            'get_else_create_many_expiries', selected_expiries=selected_expiries, created_expiries=created_expiries
        )

        return selected_expiries + created_expiries

    def __create_many_expiries(
        self, expiry_dates: Iterable[datetime], ticker_id: int, contract_size_id: int, conn: Connection
    ) -> List[Expiry]:
        logger.debug('Creating expiries', expiry_dates=expiry_dates)
        expiries = [Expiry(ticker_id=ticker_id, contract_size_id=contract_size_id, date=date) for date in expiry_dates]
        result = self.expiry_repo.insert(conn, expiries)
        return result

    def __get_expiries_with_date(self, expiry_dates: Iterable[datetime], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_dates=expiry_dates)
        expiries = [Expiry(date=date) for date in expiry_dates]
        result = self.expiry_repo.select(conn, expiries)
        return result

    @staticmethod
    def __str_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string, '%Y-%m-%d')
