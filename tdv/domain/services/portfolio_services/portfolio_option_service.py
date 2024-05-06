from typing import TYPE_CHECKING, Dict, List

from sqlalchemy import Connection

from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
from tdv.logger_setup import LoggerFactory
from tdv.utils import datetime_from_dashed_YMD_str

if TYPE_CHECKING:
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.infra.repos.portfolio_repos.portfolio_option_repo import PortfolioOptionRepo
    from tdv.domain.services.option_services.expiry_service import ExpiryService
    from tdv.domain.services.option_services.strike_service import StrikeService

logger = LoggerFactory.make_logger(__name__)


class PortfolioOptionService:
    def __init__(
        self,
        entity_cache: 'EntityCache',
        portfolio_option_repo: 'PortfolioOptionRepo',
        expiry_service: 'ExpiryService',
        strike_service: 'StrikeService',
    ) -> None:
        self.__entity_cache = entity_cache
        self.__pfol_option_repo = portfolio_option_repo
        self.__expiry_service = expiry_service
        self.__strike_service = strike_service

    def get_portfolio_options(self, portfolio_ids: List[int], conn: Connection) -> List[PortfolioOption]:
        logger.debug('Getting portfolio options', portfolio_ids=portfolio_ids)

        portfolio_options = [PortfolioOption(portfolio_id=pfol_id) for pfol_id in portfolio_ids]
        result = self.__pfol_option_repo.select(conn, portfolio_options)

        return result

    def create_local_portfolio_options(
        self, portfolio: Portfolio, options_data: List[Dict], conn: Connection
    ) -> List[PortfolioOption]:
        to_datetime = datetime_from_dashed_YMD_str

        pfol_options = []
        for option_data in options_data:
            count, expiry_date, strike_price, ticker, is_call, contract_size = (
                option_data['count'],
                to_datetime(option_data['expiry_date']),
                option_data['strike'],
                self.__entity_cache.tickers_by_name[option_data['ticker']],
                option_data['is_call'],
                self.__entity_cache.contract_sizes_by_name[option_data['size_name']],
            )

            expiry = self.__expiry_service.get_else_create_expiry(expiry_date, ticker, conn)
            strike = self.__strike_service.get_else_create_strikes(expiry, [strike_price], [contract_size], conn)[0]

            pfol_options.append(
                PortfolioOption(portfolio_id=portfolio.id, strike_id=strike.id, is_call=is_call, count=count)
            )

        result = self.__pfol_option_repo.insert(conn, pfol_options)
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
