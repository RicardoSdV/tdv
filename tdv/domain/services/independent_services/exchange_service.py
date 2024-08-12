from typing import TYPE_CHECKING

from tdv.constants import EXCHANGE
from tdv.domain.entities.independent_entities.exchange_entity import Exchange

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import Connection
    from tdv.infra.database import DB
    from tdv.infra.repos.independent_repos.exchange_repo import ExchangeRepo
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.libs.log import Logger


class ExchangeService:
    def __init__(self, db: 'DB', entity_cache: 'EntityCache', exchange_repo: 'ExchangeRepo', logger: 'Logger') -> None:
        self.__db = db
        self.__entity_cache = entity_cache
        self.__exchange_repo = exchange_repo
        self.__logger = logger

    def create_all_exchanges(self, conn: 'Connection') -> 'List[Exchange]':
        exchanges = [
            Exchange(name=name.value, long_name=long_name.value)
            for name, long_name in zip(EXCHANGE.NAME, EXCHANGE.LONG_NAME)
        ]
        self.__logger.debug('Creating all exchanges', exchanges=exchanges)
        result = self.__exchange_repo.insert(conn, exchanges)
        self.__entity_cache.cache_exchanges(exchanges)
        return result

    def get_all_exchanges(self, conn: 'Connection') -> 'List[Exchange]':
        exchanges = [Exchange(name=name.value) for name in EXCHANGE.NAME]
        self.__logger.debug('Getting all exchanges', exchanges=exchanges)
        return self.__exchange_repo.select(conn, exchanges)

    # TODO: Update __cache
    # def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
    #     logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
    #     exchanges = [Exchange(name=exchange_name)]
    #     params = {'live': is_live}
    #     with self.__db.connect as conn:
    #         result = self.exchange_repo.update(conn, exchanges, params)
    #         conn.commit()
    #     return result
