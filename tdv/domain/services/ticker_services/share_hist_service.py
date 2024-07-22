from typing import TYPE_CHECKING

from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist

if TYPE_CHECKING:
    from sqlalchemy import Connection

    from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
    from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
    from tdv.infra.repos.ticker_repos.share_hist_repo import ShareHistRepo
    from tdv.libs.log import Logger

class ShareHistService:
    def __init__(self, share_hist_repo: 'ShareHistRepo', logger: 'Logger') -> None:
        self.__share_hist_repo = share_hist_repo
        self.__logger = logger

    def create_share_hist(self, ticker: 'Ticker', insert_time: 'InsertTime', price: float, conn: 'Connection') -> 'ShareHist':
        share_hist = ShareHist(ticker_id=ticker.id, insert_time_id=insert_time.id, price=price)
        self.__logger.debug('Creating share_hist', share_hist=share_hist)
        return self.__share_hist_repo.insert(conn, [share_hist])[0]
