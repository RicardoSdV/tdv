from typing import List

from tdv.domain.entities.ticker_share_type_entity import TickerShareType
from tdv.domain.internal.db_interactive_service import DbInteractiveService
from tdv.domain.internal.ticker_service import TickerService
from tdv.infra.database import DB
from tdv.infra.repos.share_type_repo import ShareTypeRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class ShareTypeService(DbInteractiveService):
    def __init__(self, db: 'DB', share_type_repo: 'ShareTypeRepo', ticker_service: TickerService) -> None:
        super().__init__(db, share_type_repo)

        self.ticker_service = ticker_service

    def create_ticker_share_type(self, ticker_name: str, share_type: str) -> List[TickerShareType]:
        logger.debug('Creating ticker_share_type', ticker_name=ticker_name, share_type=share_type)

        tickers = self.ticker_service.get_ticker_by_name(ticker_name)
        ticker_id = tickers[0].id
        ticker_share_types = [TickerShareType(ticker_id=ticker_id, share_type=share_type)]

        ticker_share_types = self._do_db_operation(self._repo.insert, ticker_share_types)
        return ticker_share_types

    def delete_ticker_share_type(self, ticker_name: str, share_type: str) -> List[TickerShareType]:
        logger.debug('Deleting ticker_share_type', ticker_name=ticker_name, share_type=share_type)

        tickers = self.ticker_service.get_ticker_by_name(ticker_name)
        ticker_id = tickers[0].id
        ticker_share_types = [TickerShareType(ticker_id=ticker_id, share_type=share_type)]

        ticker_share_types = self._do_db_operation(self._repo.delete, ticker_share_types)
        return ticker_share_types