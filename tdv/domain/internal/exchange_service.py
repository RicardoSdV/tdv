from typing import TYPE_CHECKING

from sqlalchemy import CursorResult

from tdv.constants import ExchangeNames
from tdv.domain.entities.exchange_entity import Exchange
from tdv.logger_setup import logger_obj

if TYPE_CHECKING:
    from tdv.storage.db import DB
    from tdv.storage.exchange_repo import ExchangeRepo

logger = logger_obj.get_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        self.__db = db
        self.__exchange_repo = exchange_repo

    def create_exchange(self, exchange_name: str) -> CursorResult:
        logger.info('Creating exchange', exchange_name=exchange_name)

        exchange = Exchange(ExchangeNames.str_to_enum(exchange_name))
        with self.__db.engine.connect() as conn:
            result = self.__exchange_repo.insert(conn, exchange)
            conn.commit()

        return result

    def create_all_exchanges(self) -> CursorResult:
        exchange_names = ExchangeNames.to_dict()
        logger.info('Creating all exchanges', **exchange_names)

        exchanges = [Exchange(ExchangeNames.str_to_enum(name)) for name in exchange_names.values()]
        with self.__db.engine.connect() as conn:
            result = self.__exchange_repo.insert_many(conn, exchanges)
            conn.commit()

        return result
