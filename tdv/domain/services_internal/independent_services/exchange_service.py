from typing import TYPE_CHECKING, List

from sqlalchemy import Connection

from tdv.constants import Exchanges
from tdv.domain.entities.independent_entities.exchange_entity import Exchange
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.independent_repos.exchange_repo import ExchangeRepo

logger = LoggerFactory.make_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        self.db = db
        self.exchange_repo = exchange_repo

    def create_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [
            Exchange(name=name.value, long_name=long_name.value)
            for name, long_name in zip(Exchanges.ShortNames, Exchanges.LongNames)
        ]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        result = self.exchange_repo.insert(conn, exchanges)
        return result

    def get_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in Exchanges.ShortNames]
        logger.debug('Getting all exchanges', exchanges=exchanges)
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