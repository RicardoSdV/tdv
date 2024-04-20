from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Connection

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
        with self.db.connect as conn:
            exchange = [Exchange(name=exchange_name)]
            if self.exchange_repo.select(conn, exchange):
                logger.info('Exchange already exists', exchange_name=exchange_name)
                return []

            result = self.exchange_repo.insert(conn, exchange)
            conn.commit()
        return result

    def create_all_exchanges(self) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        with self.db.connect as conn:
            existing_exchanges = self.exchange_repo.select(conn, exchanges)
            existing_names = set(ex.name for ex in existing_exchanges)

            new_exchanges = [ex for ex in exchanges if ex.name not in existing_names]

            if new_exchanges:
                result = self.exchange_repo.insert(conn, new_exchanges)
                conn.commit()
                logger.info('New exchanges added', exchanges=new_exchanges)
            else:
                logger.info('No new exchanges to add')
                result = None
                conn.commit()
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

    def get_all_exchanges(self) -> List[Exchange]:
        logger.debug('Getting all exchanges')
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        with self.db.connect as conn:
            result = self.exchange_repo.select(conn, exchanges)
            conn.commit()
        return result

    def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
        logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
        exchanges = [Exchange(name=exchange_name)]
        params = {'live': is_live}
        with self.db.connect as conn:
            result = self.exchange_repo.update(conn, exchanges, params)
            conn.commit()
        return result

    def delete_exchange_by_id(self, exchange_id: int) -> List[Exchange]:
        logger.debug('Deleting exchange by id', exchange_id=exchange_id)
        exchanges = [Exchange(exchange_id=exchange_id)]
        with self.db.connect as conn:
            result = self.exchange_repo.delete(conn, exchanges)
            conn.commit()
        return result

    def delete_exchange_by_name(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Deleting exchange by name', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        with self.db.connect as conn:
            result = self.exchange_repo.delete(conn, exchanges)
            conn.commit()
        return result

    def delete_all_exchanges(self) -> List[Exchange]:
        logger.debug('Deleting all exchanges')
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        with self.db.connect as conn:
            result = self.exchange_repo.delete(conn, exchanges)
            conn.commit()
        return result
