from typing import List, TYPE_CHECKING, Tuple

from sqlalchemy import Connection

from local_user_data.portfolio_data import local_user_portfolio_data
from tdv.domain.entities.independent_entities.account_entity import Account
from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
from tdv.domain.entities.portfolio_entities.portfolio_share_entity import PortfolioShare
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.portfolio_repos.portfolio_repo import PortfolioRepo
    from tdv.domain.cache.cache_service import CacheService
    from tdv.domain.services.portfolio_services.portfolio_share_service import PortfolioShareService
    from tdv.domain.services.portfolio_services.portfolio_option_service import PortfolioOptionService

logger = LoggerFactory.make_logger(__name__)

PfolCombo = Tuple[List[Portfolio], List[PortfolioShare], List[PortfolioOption]]


class PortfolioService:
    def __init__(
        self,
        portfolio_repo: 'PortfolioRepo',
        cache_service: 'CacheService',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
    ) -> None:
        self.__portfolio_repo = portfolio_repo
        self.__cache_service = cache_service
        self.__pfol_share_service = pfol_share_service
        self.__pfol_option_service = pfol_option_service

    def create_all_local_user_portfolios(self, account: Account, conn: Connection) -> PfolCombo:
        portfolios, pfol_shares, pfol_options = [], [], []
        for name, data in local_user_portfolio_data.items():
            cash, shares_data, options_data = data['cash'], data['shares'], data['options_data']

            portfolio_for_insert = Portfolio(account_id=account.id, name=name, cash=cash)
            inserted_portfolio = self.__portfolio_repo.insert(conn, [portfolio_for_insert])[0]

            inserted_pfol_shares = self.__pfol_share_service.create_local_portfolio_shares(inserted_portfolio, shares_data, conn)
            inserted_pfol_options = self.__pfol_option_service.create_local_portfolio_options(
                inserted_portfolio, options_data, conn
            )

            portfolios.append(inserted_portfolio)
            pfol_shares.extend(inserted_pfol_shares)
            pfol_options.extend(inserted_pfol_options)

        return portfolios, pfol_shares, pfol_options

    def get_portfolios_with_account_id(self, account_id: int, conn: Connection) -> List[Portfolio]:
        logger.debug('Getting portfolios', account_id=account_id)
        portfolios = self.__portfolio_repo.select(conn, [Portfolio(account_id=account_id)])
        return portfolios

    def create_many_portfolios(
        self, account_id: int, names: List[str], cashes: List[float], conn: Connection
    ) -> List[Portfolio]:
        logger.debug('Creating test portfolio', account_id=account_id, names=names, cashes=cashes)
        portfolios = [Portfolio(account_id=account_id, name=name, cash=cash) for name, cash in zip(names, cashes)]
        result = self.__portfolio_repo.insert(conn, portfolios)
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
