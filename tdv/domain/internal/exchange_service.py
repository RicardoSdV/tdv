from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Connection

from tdv.constants import TICKERS_BY_EXCHANGE
from tdv.domain.entities.exchange_entity import Exchanges, Exchange
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.exchange_repo import ExchangeRepo

logger = LoggerFactory.make_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        self.db = db
        self.exchange_repo = exchange_repo

    def create_exchange(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Creating exchange', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        with self.db.connect as conn:
            result = self.exchange_repo.insert(conn, exchanges)
            conn.commit()
        return result

    def create_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [Exchange(name=name) for name in TICKERS_BY_EXCHANGE]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        result = self.exchange_repo.insert(conn, exchanges)
        return result

    def get_exchange_by_id(self, exchange_id: int) -> List[Exchange]:
        logger.debug('Getting exchange by id', exchange_id=exchange_id)
        exchanges = [Exchange(exchange_id=exchange_id)]
        with self.db.connect as conn:
            result = self.exchange_repo.select(conn, exchanges)
            conn.commit()
        return result

    def get_exchange_by_name(self, exchange_name: str, conn: Optional[Connection] = None) -> List[Exchange]:
        logger.debug('Getting exchange by name', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]

        if conn is None:
            with self.db.connect as conn:
                result = self.exchange_repo.select(conn, exchanges)
                conn.commit()
        else:
            result = self.exchange_repo.select(conn, exchanges)

        return result

    def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
        logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
        exchanges = [Exchange(name=exchange_name)]
        params = {'live': is_live}
        with self.db.connect as conn:
            result = self.exchange_repo.update(conn, exchanges, params)
            conn.commit()
        return result

    def delete_exchange_by_name(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Deleting exchange by name', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        with self.db.connect as conn:
            result = self.exchange_repo.delete(conn, exchanges)
            conn.commit()
        return result
