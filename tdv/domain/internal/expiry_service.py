from typing import List, TYPE_CHECKING, Iterator

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

    def get_expiries(self, expiry_ids: Iterator[int], conn: Connection) -> List[Expiry]:
        logger.debug('Getting expiries', expiry_ids=expiry_ids)
        expiries = [Expiry(expiry_id=_id) for _id in expiry_ids]
        result = self.expiry_repo.select(conn, expiries)
        return result
