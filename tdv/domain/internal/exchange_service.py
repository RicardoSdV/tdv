from tdv.domain.data_types import ExchangeName
from tdv.logger_setup import logger_obj
from tdv.storage import DB
from tdv.storage.exchange_repo import ExchangeRepo

logger = logger_obj.get_logger(__name__)


class ExchangeService:
    def __init__(self, db: DB, exchange_repo: ExchangeRepo) -> None:
        self.__db = db
        self.__exchange_repo = exchange_repo

    def create_exchange(self, exchange_name: ExchangeName) -> None:
        logger