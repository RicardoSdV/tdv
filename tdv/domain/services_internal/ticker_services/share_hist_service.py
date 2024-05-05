from typing import TYPE_CHECKING

from sqlalchemy import Connection

from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist
from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.ticker_repos.share_hist_repo import ShareHistRepo

logger = LoggerFactory.make_logger(__name__)


class ShareHistService:
    def __init__(self, share_hist_repo: 'ShareHistRepo') -> None:
        self.__share_hist_repo = share_hist_repo

    def create_share_hist(self, ticker: Ticker, insert_time: InsertTime, price: float, conn: Connection) -> ShareHist:
        share_hist = ShareHist(ticker_id=ticker.id, insert_time_id=insert_time.id, price=price)
        logger.debug('Creating share_hist', share_hist=share_hist)
        result = self.__share_hist_repo.insert(conn, [share_hist])
        return result[0]
