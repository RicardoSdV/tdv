from typing import Optional, List

from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.infra.database import DB
from tdv.infra.repos.portfolio_shares_repo import PortfolioSharesRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class PortfolioSharesService:
    def __init__(
        self,
        db: 'DB',
        portfolio_shares_repo: 'PortfolioSharesRepo',
        ticker_repo: 'TickerService',
        share_type_repo: 'ShareTypeService',
    ) -> None:
        self.db = db
        self.portfolio_shares_repo = portfolio_shares_repo
        self.ticker_repo = ticker_repo
        self.share_type_repo = share_type_repo

    def create(
        self,
        portfolio_id: int,
        ticker: str,
        ticker_share_type_id: int,
        count: Optional[float],
    ) -> List[PortfolioShare]:
        logger.debug(
            'Creating portfolio_shares',
            portfolio_id=portfolio_id,
            ticker=ticker,
            ticker_share_type_id=ticker_share_type_id,
            count=count,
        )
        portfolio_shares = [
            PortfolioShare(
                portfolio_id=portfolio_id,
                ticker=ticker,
                ticker_share_type_id=ticker_share_type_id,
                count=count,
            )
        ]
        with self.db.connect as conn:
            result = self.portfolio_shares_repo.insert(conn, portfolio_shares)
            conn.commit()
        return result

    # def get_portfolio_shares_by_user_id_and_portfolio_id(self, user_id: int, portfolio_id: int) -> List[PortfolioShare]:
    #     logger.debug('Getting user_shares by user_id and portfolio_id', user_id=user_id, portfolio_id=portfolio_id)
    #     portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id)]
    #     with self.db.connect as conn:
    #         result = self.portfolio_shares_repo.select(conn, portfolio_shares)
    #         conn.commit()
    #     return result
    #
    # def update_count_by_user_id_and_share_type(self, user_id: int, portfolio_id: int, ticker: str, share_type: str,
    #                                            count: float) -> List[PortfolioShare]:
    #     logger.debug('Updating user_shares count', user_id=user_id, portfolio_id=portfolio_id, ticker=ticker, share_type=share_type,
    #                  new_count=count)
    #     params = {'count': count}
    #     with self.db.connect as conn:
    #         tickers = self.ticker_service.get_ticker_by_name(ticker, conn)
    #         ticker_id = tickers[0].id
    #         assert isinstance(ticker_id, int)
    #         ticker_share_types = self.share_type_service.get_ticker_share_type_by_ticker_id(ticker_id, conn)
    #         ticker_share_type_id = ticker_share_types[0].id
    #         portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id, ticker_share_type_id=ticker_share_type_id)]
    #         result = self.portfolio_shares_repo.update(conn, portfolio_shares, params)
    #         conn.commit()
    #     return result
    #
    # def delete_portfolio_shares_by_user_id_and_portfolio_id(self, user_id: int, portfolio_id: int) -> List[PortfolioShare]:
    #     logger.debug('Deleting portfolio_shares', user_id=user_id, portfolio_id=portfolio_id)
    #     portfolio_shares = [PortfolioShare(user_id=user_id, portfolio_id=portfolio_id)]
    #     with self.db.connect as conn:
    #         result = self.portfolio_shares_repo.delete(conn, portfolio_shares)
    #         conn.commit()
    #     return result
