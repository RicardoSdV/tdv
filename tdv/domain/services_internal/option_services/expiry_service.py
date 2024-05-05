from datetime import datetime
from typing import List, TYPE_CHECKING, Generator
from sqlalchemy import Connection

from tdv.domain.entities.option_entities.expiry_entity import Expiry
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.option_repos.expiry_repo import ExpiryRepo

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
        expiry = [Expiry(date=expiry_date, ticker_id=ticker_id)]

        logger.debug('Getting expiry', expiry=expiry)
        selected_expiries = self.expiry_repo.select(conn, expiry)
        if len(selected_expiries) > 0:
            return selected_expiries[0]

        logger.debug('Expiry not found, creating expiry', expiry=expiry)
        created_expiries = self.expiry_repo.insert(conn, expiry)

        return created_expiries[0]
