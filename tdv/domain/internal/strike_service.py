from typing import List, TYPE_CHECKING, Iterator

from sqlalchemy import Connection

from tdv.domain.entities.strike_entity import Strike
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.strike_repo import StrikeRepo

logger = LoggerFactory.make_logger(__name__)


class StrikeService:
    def __init__(self, db: DB, strike_repo: StrikeRepo) -> None:
        self.db = db
        self.strike_repo = strike_repo

    def get_strikes(self, strike_ids: Iterator[int], conn: Connection) -> List[Strike]:
        logger.debug('Getting strikes', strike_ids=strike_ids)
        strikes = [Strike(strike_id=_id) for _id in strike_ids]
        result = self.strike_repo.select(conn, strikes)
        return result
