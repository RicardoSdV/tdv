from typing import TYPE_CHECKING, List

from tdv.domain.entities.exchange import Exchanges, Exchange
from tdv.logger_setup import logger_obj

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.exchange_repo import ExchangeRepo

logger = logger_obj.get_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        self.__db = db
        self.__exchange_repo = exchange_repo

    def create_exchange(self, exchange_name: str) -> List[Exchange]:
        logger.info('Creating exchange', exchange_name=exchange_name)

        exchange = Exchange(name=exchange_name)
        with self.__db.connect as conn:
            result = self.__exchange_repo.insert(conn, [exchange])
            conn.commit()

        return result

    def create_all_exchanges(self) -> List[Exchange]:
        exchanges = [Exchange(name=name) for name in Exchanges]
        logger.info('Creating all exchanges', exchanges)

        with self.__db.connect as conn:
            result = self.__exchange_repo.insert(conn, exchanges)
            conn.commit()

        return result

    def get_exchange_by_id(self, exchange_id: int) -> Exchange:
        logger.info('Getting exchange by id', exchange_id=exchange_id)

        with self.__db.connect as conn:
            exchange: Exchange = self.__exchange_repo.get_or_raise_by_id(exchange_id)
            conn.commit()

        return exchange

    def get_exchange_by_name(self, exchange_name: str) -> Exchange:
        logger.info('Getting exchange by name', exchange_name=exchange_name)

        with self.__db.connect as conn:
            exchange: Exchange = self.__exchange_repo.get_or_raise_by_name(exchange_name)
            conn.commit()

        return exchange
