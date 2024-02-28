from typing import TYPE_CHECKING, List

from tdv.domain.entities.exchange_entity import Exchanges, Exchange
from tdv.domain.internal.db_interactive_service import DbInteractiveService
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.exchange_repo import ExchangeRepo

logger = LoggerFactory.make_logger(__name__)


class ExchangesService(DbInteractiveService):
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo') -> None:
        super().__init__(db, exchange_repo)

    def create_exchange(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Creating exchange', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        exchanges = self._do_db_operation(self._repo.insert, exchanges)
        return exchanges

    def create_all_exchanges(self) -> List[Exchange]:
        exchanges = [Exchange(name=name.value) for name in Exchanges]
        logger.debug('Creating all exchanges', exchanges=exchanges)
        exchanges = self._do_db_operation(self._repo.insert, exchanges)
        return exchanges

    def get_exchange_by_id(self, exchange_id: int) -> List[Exchange]:
        logger.debug('Getting exchange by id', exchange_id=exchange_id)
        exchanges = [Exchange(exchange_id=exchange_id)]
        exchanges = self._do_db_operation(self._repo.select, exchanges)
        return exchanges

    def get_exchange_by_name(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Getting exchange by name', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        exchanges = self._do_db_operation(self._repo.select, exchanges)
        return exchanges

    def update_exchange_live(self, exchange_name: str, is_live: bool) -> List[Exchange]:
        logger.debug('Updating exchange live status', exchange_name=exchange_name, is_live=is_live)
        exchanges = [Exchange(name=exchange_name, live=is_live)]
        exchanges = self._do_db_operation(self._repo.update, exchanges)
        return exchanges

    def delete_exchange_by_name(self, exchange_name: str) -> List[Exchange]:
        logger.debug('Deleting exchange by name', exchange_name=exchange_name)
        exchanges = [Exchange(name=exchange_name)]
        exchanges = self._do_db_operation(self._repo.delete, exchanges)
        return exchanges
