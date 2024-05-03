from typing import TYPE_CHECKING, Dict, List, Iterable, Sequence

from psycopg import Connection

from tdv.domain.entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.portfolio_option_repo import PortfolioOptionRepo

logger = LoggerFactory.make_logger(__name__)


class PortfolioOptionService:
    def __init__(self, db: 'DB', portfolio_option_repo: 'PortfolioOptionRepo') -> None:
        self.db = db
        self.pfol_option_repo = portfolio_option_repo

    def get_portfolio_options(self, portfolio_ids: List[int], conn: Connection) -> List[PortfolioOption]:
        logger.debug('Getting portfolio options', portfolio_ids=portfolio_ids)

        portfolio_options = [PortfolioOption(portfolio_id=pfol_id) for pfol_id in portfolio_ids]
        result = self.pfol_option_repo.select(conn, portfolio_options)

        return result

    # def create_portfolio_options(
    #     self, portfolio_id: int, option_id: int, count: Optional[float]
    # ) -> List[PortfolioOption]:
    #     logger.debug(
    #         'Creating user_options',
    #         portfolio_id=portfolio_id,
    #         option_id=option_id,
    #         count=count,
    #     )
    #     portfolio_options = [PortfolioOption(portfolio_id=portfolio_id, option_id=option_id, count=count)]
    #
    #     with self.db.connect as conn:
    #         result = self.portfolio_options_repo.insert(conn, portfolio_options)
    #         conn.commit()
    #     return result
    #
    # def get_portfolio_options_by_user_id_and_portfolio_id(
    #     self, account_id: int, portfolio_id: int
    # ) -> List[PortfolioOption]:
    #     logger.debug(
    #         'Getting user_options by user_id and option_id',
    #         account_id=account_id,
    #         portfolio_id=portfolio_id,
    #     )
    #     portfolio_options = [PortfolioOption(account_id=account_id, portfolio_id=portfolio_id)]
    #     with self.db.connect as conn:
    #         result = self.portfolio_options_repo.select(conn, portfolio_options)
    #         conn.commit()
    #     return result
    #
    # def update_count_by_user_id_and_option_id(
    #     self, user_id: int, option_id: int, count: float
    # ) -> List[PortfolioOption]:
    #     logger.debug(
    #         'Updating user_options count',
    #         user_id=user_id,
    #         option_id=option_id,
    #         new_count=count,
    #     )
    #     portfolio_options = [PortfolioOption(user_id=user_id, option_id=option_id, count=count)]
    #     with self.db.connect as conn:
    #         result = self.user_options_repo.update(conn, portfolio_options=portfolio_options)
    #         conn.commit()
    #     return result
    #
    # def delete_portfolio_option_by_option_id(
    #     self, user_id: int, portfolio_id: int, option_id: int
    # ) -> List[PortfolioOption]:
    #     logger.debug(
    #         'Deleting user_options',
    #         user_id=user_id,
    #         portfolio_id=portfolio_id,
    #         option_id=option_id
    #     )
    #     user_options = [PortfolioOption(user_id=user_id, portfolio_id=portfolio_id, option_id=option_id)]
    #     with self.db.connect as conn:
    #         result = self.user_options_repo.delete(conn, user_options)
    #         conn.commit()
    #     return result
