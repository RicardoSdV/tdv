from typing import List, Optional

from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.infra.database import DB
from tdv.infra.repos.portfolio_options_repo import PortfolioOptionsRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class PortfolioOptionsService:
    def __init__(self, db: 'DB', portfolio_options_repo: 'PortfolioOptionsRepo') -> None:
        self.db = db
        self.portfolio_options_repo = portfolio_options_repo

    def create_portfolio_options(self, portfolio_id: int, option_id: int, count: Optional[float]) -> List[PortfolioOption]:
        logger.debug('Creating user_options', portfolio_id=portfolio_id, option_id=option_id, count=count)
        portfolio_options = [PortfolioOption(portfolio_id=portfolio_id, option_id=option_id, count=count)]

        with self.db.connect as conn:
            result = self.portfolio_options_repo.insert(conn, portfolio_options)
            conn.commit()
        return result

    def get_portfolio_options_by_user_id_and_portfolio_id(self, user_id: int, portfolio_id: int) -> List[PortfolioOption]:
        logger.debug('Getting user_options by user_id and option_id', user_id=user_id, portfolio_id=portfolio_id)
        portfolio_options = [PortfolioOption(user_id=user_id, portfolio_id=portfolio_id)]
        with self.db.connect as conn:
            result = self.portfolio_options_repo.select(conn, portfolio_options)
            conn.commit()
        return result

    def update_count_by_user_id_and_option_id(self, user_id: int, option_id: int, count: float) -> List[PortfolioOption]:
        logger.debug('Updating user_options count', user_id=user_id, option_id=option_id, new_count=count)
        portfolio_options = [PortfolioOption(user_id=user_id, option_id=option_id, count=count)]
        with self.db.connect as conn:
            result = self.user_options_repo.update(conn, portfolio_options=portfolio_options)
            conn.commit()
        return result

    def delete_portfolio_option_by_option_id(self, user_id: int, portfolio_id: int, option_id: int) -> List[PortfolioOption]:
        logger.debug('Deleting user_options', user_id=user_id, portfolio_id=portfolio_id, option_id=option_id)
        user_options = [PortfolioOption(user_id=user_id, portfolio_id=portfolio_id, option_id=option_id)]
        with self.db.connect as conn:
            result = self.user_options_repo.delete(conn, user_options)
            conn.commit()
        return result
