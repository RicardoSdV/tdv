from typing import List

from sqlalchemy import Connection

from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.infra.database import DB
from tdv.infra.repos.portfolio_share_repo import PortfolioShareRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class PortfolioShareService:
    def __init__(self, db: 'DB', pfol_share_repo: PortfolioShareRepo) -> None:
        self.db = db
        self.pfol_share_repo = pfol_share_repo

    def get_portfolio_shares(self, pfol_ids: List[int], conn: Connection) -> List[PortfolioShare]:
        logger.debug('Getting portfolio shares', portfolio_ids=pfol_ids)
        pfol_shares = [PortfolioShare(portfolio_id=pfol_id) for pfol_id in pfol_ids]
        result = self.pfol_share_repo.select(conn, pfol_shares)
        return result

    def create_many_portfolio_shares(self, portfolio_id: List[int], ticker_id: int, count: List[float], conn: Connection) -> List[PortfolioShare]:
        logger.debug('Creating test portfolio shares', portfolio_id=portfolio_id, ticker_id=ticker_id, count=count)
        shares = [PortfolioShare(portfolio_id=portfolio_id, ticker_id=ticker_id, count=count) for portfolio_id, count in zip(portfolio_id, count)]
        result = self.pfol_share_repo.insert(conn, shares)
        return result


#     def create(
#         self,
#         portfolio_id: int,
#         ticker: str,
#         ticker_share_type_id: int,
#         count: Optional[float],
#     ) -> List[PortfolioShare]:
#         logger.debug(
#             'Creating portfolio_shares',
#             portfolio_id=portfolio_id,
#             ticker=ticker,
#             ticker_share_type_id=ticker_share_type_id,
#             count=count,
#         )
#         portfolio_shares = [
#             PortfolioShare(
#                 portfolio_id=portfolio_id,
#                 ticker=ticker,
#                 ticker_share_type_id=ticker_share_type_id,
#                 count=count,
#             )
#         ]
#         with self.db.connect as conn:
#             result = self.portfolio_shares_repo.insert(conn, portfolio_shares)
#             conn.commit()
#         return result
#
#     # def get_portfolio_shares_by_user_id_and_portfolio_id(self, user_id: int, portfolio_id: int) -> List[PortfolioShare]:
#     #     logger.debug('Getting user_shares by user_id and portfolio_id', user_id=user_id, portfolio_id=portfolio_id)
#     #     portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id)]
#     #     with self.db.connect as conn:
#     #         result = self.portfolio_shares_repo.select(conn, portfolio_shares)
#     #         conn.commit()
#     #     return result
#     #
#     # def update_count_by_user_id_and_share_type(self, user_id: int, portfolio_id: int, ticker: str, share_type: str,
#     #                                            count: float) -> List[PortfolioShare]:
#     #     logger.debug('Updating user_shares count', user_id=user_id, portfolio_id=portfolio_id, ticker=ticker, share_type=share_type,
#     #                  new_count=count)
#     #     params = {'count': count}
#     #     with self.db.connect as conn:
#     #         tickers = self.ticker_service.get_ticker_by_name(ticker, conn)
#     #         ticker_id = tickers[0].id
#     #         assert isinstance(ticker_id, int)
#     #         ticker_share_types = self.share_type_service.get_ticker_share_type_by_ticker_id(ticker_id, conn)
#     #         ticker_share_type_id = ticker_share_types[0].id
#     #         portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id, ticker_share_type_id=ticker_share_type_id)]
#     #         result = self.portfolio_shares_repo.update(conn, portfolio_shares, params)
#     #         conn.commit()
#     #     return result
#     #
#     # def delete_portfolio_shares_by_user_id_and_portfolio_id(self, user_id: int, portfolio_id: int) -> List[PortfolioShare]:
#     #     logger.debug('Deleting portfolio_shares', user_id=user_id, portfolio_id=portfolio_id)
#     #     portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id)]
#     #     with self.db.connect as conn:
#     #         result = self.portfolio_shares_repo.delete(conn, portfolio_shares)
#     #         conn.commit()
#     #     return result
