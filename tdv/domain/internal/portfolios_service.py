from typing import List

from tdv.domain.entities.portfolios_entity import Portfolios
from tdv.infra.database import DB
from tdv.infra.repos.portfolios_repo import PortfoliosRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class PortfoliosService:
    def __init__(self, db: 'DB', portfolios_repo: 'PortfoliosRepo') -> None:
        self.db = db
        self.portfolios_repo = portfolios_repo

    def create_portfolio(self, user_id: int, cash: float) -> List[Portfolios]:
        logger.debug('Creating portfolio', user_id=user_id, cash=cash)
        portfolios = [Portfolios(user_id=user_id, cash=cash)]
        with self.db.connect as conn:
            result = self.portfolios_repo.insert(conn, portfolios)
            conn.commit()
        return result

    def create_portfolio_shares(self, portfolio_id: int, portfolio_shares_id: int) -> List[Portfolios]:
        logger.debug('Creating portfolio shares', portfolio_id=portfolio_id, portfolio_shares_id=portfolio_shares_id)
        portfolios = [Portfolios(portfolio_id=portfolio_id, portfolio_shares_id=portfolio_shares_id)]
        with self.db.connect as conn:
            result = self.portfolios_repo.insert(conn, portfolios)
            conn.commit()
        return result

    def delete_portfolio(self, portfolio_id: int) -> List[Portfolios]:
        logger.debug('Deleting portfolio', portfolio_id=portfolio_id)
        portfolios = [Portfolios(portfolio_id=portfolio_id)]
        with self.db.connect as conn:
            result = self.portfolios_repo.delete(conn, portfolios)
            conn.commit()
        return result
