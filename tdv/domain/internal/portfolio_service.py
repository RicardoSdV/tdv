from typing import List, TYPE_CHECKING

from tdv.domain.entities.portfolio_entity import Portfolio

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.domain.internal.session_service import SessionService
    from tdv.infra.database import DB
    from tdv.infra.repos.portfolios_repo import PortfolioRepo


logger = LoggerFactory.make_logger(__name__)


class PortfolioService:
    def __init__(self, db: 'DB', portfolio_repo: 'PortfolioRepo', session_service: 'SessionService') -> None:
        self.db = db
        self.portfolio_repo = portfolio_repo
        self.session_service = session_service

    def create_portfolio(self) -> List[Portfolio]:
        current_user_id = self.session_service.current_session_user_id

        logger.debug('Creating portfolio', current_user_id=current_user_id)
        portfolios = [Portfolio(user_id=current_user_id)]
        with self.db.connect as conn:
            result = self.portfolio_repo.insert(conn, portfolios)
            conn.commit()
        return result

    def create_portfolio_shares(self, portfolio_id: int, portfolio_shares_id: int) -> List[Portfolio]:
        logger.debug(
            'Creating portfolio shares',
            portfolio_id=portfolio_id,
            portfolio_shares_id=portfolio_shares_id,
        )
        portfolios = [Portfolio(portfolio_id=portfolio_id, portfolio_shares_id=portfolio_shares_id)]
        with self.db.connect as conn:
            result = self.portfolio_repo.insert(conn, portfolios)
            conn.commit()
        return result

    def delete_portfolio(self, portfolio_id: int) -> List[Portfolio]:
        logger.debug('Deleting portfolio', portfolio_id=portfolio_id)
        portfolios = [Portfolio(portfolio_id=portfolio_id)]
        with self.db.connect as conn:
            result = self.portfolio_repo.delete(conn, portfolios)
            conn.commit()
        return result
