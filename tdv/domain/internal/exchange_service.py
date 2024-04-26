from typing import TYPE_CHECKING, List, Optional, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.exchange_entity import Exchange, Exchanges
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.exchange_repo import ExchangeRepo

logger = LoggerFactory.make_logger(__name__)


class ExchangeService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        self.db = db
        self.exchange_repo = exchange_repo

        self.__exchanges: Tuple[Exchange, ...] = ()

    @property
    def exchanges(self) -> Tuple[Exchange, ...]:
        if not self.__exchanges:
            self.__exchanges = tuple(self.get_all_exchanges())

        return self.__exchanges

    def create_all_exchanges(self, conn: Connection) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        result = self.exchange_repo.insert(conn, exchanges)
        return result

    def get_all_exchanges(self) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        logger.debug('Getting all exchanges', exchanges=exchanges)

        with self.db.connect as conn:
            result = self.exchange_repo.select(conn, exchanges)
        return result

    def get_exchange_by_id(self, exchange_id: int) -> Optional[Exchange]:
        for exchange in self.exchanges:
            if exchange.id == exchange_id:
                return exchange

    def get_exchange_by_name(self, exchange_name: str) -> Optional[Exchange]:
        for exchange in self.exchanges:
            if exchange.name == exchange_name:
                return exchange

    def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
        logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
        exchanges = [Exchange(name=exchange_name)]
        params = {'live': is_live}
        with self.db.connect as conn:
            result = self.exchange_repo.update(conn, exchanges, params)
            conn.commit()
        self.__exchanges = ()
        return result
