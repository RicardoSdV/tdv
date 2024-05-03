from typing import List, TYPE_CHECKING, Dict

from sqlalchemy import Connection

from sqlalchemy import Connection

from tdv.domain.entities.portfolio_entity import Portfolio

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.portfolio_repo import PortfolioRepo


logger = LoggerFactory.make_logger(__name__)


class PortfolioService:
    def __init__(self, db: 'DB', portfolio_repo: 'PortfolioRepo') -> None:
        self.db = db
        self.portfolio_repo = portfolio_repo

    def create_portfolio(self, account_id: int, portfolio_name: str) -> List[Portfolio]:
        logger.debug('Creating portfolio', account_id=account_id, portfolio_name=portfolio_name)
        portfolios = [Portfolio(account_id=account_id, name=portfolio_name)]

        with self.db.connect as conn:
            result = self.portfolio_repo.insert(conn, portfolios)
            conn.commit()
        return result

    def get_portfolios_with_account_id(self, account_id: int, conn: Connection) -> List[Portfolio]:
        logger.debug('Getting portfolios', account_id=account_id)
        portfolios = self.portfolio_repo.select(conn, [Portfolio(account_id=account_id)])
        return portfolios

    def create_many_portfolios(
        self, account_id: int, names: List[str], cashes: List[float], conn: Connection
    ) -> List[Portfolio]:
        logger.debug('Creating test portfolio', account_id=account_id, names=names, cashes=cashes)
        portfolios = [Portfolio(account_id=account_id, name=name, cash=cash) for name, cash in zip(names, cashes)]
        result = self.portfolio_repo.insert(conn, portfolios)
        return result

    # def create_portfolio_shares(self, portfolio_id: int, portfolio_shares_id: int) -> List[Portfolio]:
    #     logger.debug(
    #         'Creating portfolio shares',
    #         portfolio_id=portfolio_id,
    #         portfolio_shares_id=portfolio_shares_id,
    #     )
    #     portfolios = [Portfolio(portfolio_id=portfolio_id, portfolio_shares_id=portfolio_shares_id)]
    #     with self.db.connect as conn:
    #         result = self.portfolio_repo.insert(conn, portfolios)
    #         conn.commit()
    #     return result
    #
    # def delete_portfolio(self, portfolio_id: int) -> List[Portfolio]:
    #     logger.debug('Deleting portfolio', portfolio_id=portfolio_id)
    #     portfolios = [Portfolio(portfolio_id=portfolio_id)]
    #     with self.db.connect as conn:
    #         result = self.portfolio_repo.delete(conn, portfolios)
    #         conn.commit()
    #     return result
