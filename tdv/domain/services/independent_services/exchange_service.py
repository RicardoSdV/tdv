from typing import TYPE_CHECKING, List

from sqlalchemy import Connection

from tdv.constants import EXCHANGE

from tdv.domain.entities.independent_entities.exchange_entity import Exchange
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.independent_repos.exchange_repo import ExchangeRepo
    from tdv.domain.cache.entity_cache import EntityCache

logger = LoggerFactory.make_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', entity_cache: 'EntityCache', exchange_repo: 'ExchangeRepo') -> None:
        self.__db = db
        self.__entity_cache = entity_cache
        self.__exchange_repo = exchange_repo

    def create_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [
            Exchange(name=name.value, long_name=long_name.value)
            for name, long_name in zip(EXCHANGE.NAME, EXCHANGE.LONG_NAME)
        ]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        result = self.__exchange_repo.insert(conn, exchanges)
        self.__entity_cache.cache_exchanges(exchanges)
        return result

    def get_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in EXCHANGE.NAME]
        logger.debug('Getting all exchanges', exchanges=exchanges)
        result = self.__exchange_repo.select(conn, exchanges)
        return result

    # TODO: Update cache
    # def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
    #     logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
    #     exchanges = [Exchange(name=exchange_name)]
    #     params = {'live': is_live}
    #     with self.__db.connect as conn:
    #         result = self.exchange_repo.update(conn, exchanges, params)
    #         conn.commit()
    #     return result
