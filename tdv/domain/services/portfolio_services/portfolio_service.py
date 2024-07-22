from typing import TYPE_CHECKING

from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import Connection
    from tdv.domain.entities.independent_entities.account_entity import Account
    from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
    from tdv.domain.entities.portfolio_entities.portfolio_share_entity import PortfolioShare
    from tdv.domain.services.portfolio_services.portfolio_share_service import PortfolioShareService
    from tdv.domain.services.portfolio_services.portfolio_option_service import PortfolioOptionService
    from tdv.infra.repos.portfolio_repos.portfolio_repo import PortfolioRepo
    from tdv.libs.log import Logger

    PfolCombo = Tuple[List[Portfolio], List[PortfolioShare], List[PortfolioOption]]


class PortfolioService:
    def __init__(
        self,
        portfolio_repo: 'PortfolioRepo',
        pfol_share_service: 'PortfolioShareService',
        pfol_option_service: 'PortfolioOptionService',
        logger: 'Logger',
    ) -> None:
        self.__portfolio_repo = portfolio_repo
        self.__pfol_share_service = pfol_share_service
        self.__pfol_option_service = pfol_option_service
        self.__logger = logger

    def create_all_local_user_portfolios(self, account: 'Account', conn: 'Connection') -> 'PfolCombo':
        from local_user_data.portfolio_data import local_user_portfolio_data

        portfolios, pfol_shares, pfol_options = [], [], []
        for name, data in local_user_portfolio_data.items():
            cash, shares_data, options_data = data['cash'], data['shares'], data['options_data']

            portfolio_for_insert = Portfolio(account_id=account.id, name=name, cash=cash)
            inserted_portfolio = self.__portfolio_repo.insert(conn, [portfolio_for_insert])[0]

            inserted_pfol_shares = self.__pfol_share_service.create_local_portfolio_shares(
                inserted_portfolio, shares_data, conn

            )
            inserted_pfol_options = self.__pfol_option_service.create_local_portfolio_options(
                inserted_portfolio, options_data, conn
            )

            portfolios.append(inserted_portfolio)
            pfol_shares.extend(inserted_pfol_shares)
            pfol_options.extend(inserted_pfol_options)

        return portfolios, pfol_shares, pfol_options

    def get_portfolios_with_account_id(self, account_id: int, conn: 'Connection') -> 'List[Portfolio]':
        self.__logger.debug('Getting portfolios', account_id=account_id)
        return self.__portfolio_repo.select(conn, [Portfolio(account_id=account_id)])

    def create_many_portfolios(
        self, account_id: int, names: 'List[str]', cashes: 'List[float]', conn: 'Connection'
    ) -> 'List[Portfolio]':
        self.__logger.debug('Creating test portfolio', account_id=account_id, names=names, cashes=cashes)
        return self.__portfolio_repo.insert(
            conn,
            entities=[
                Portfolio(account_id=account_id, name=name, cash=cash)
                for name, cash in zip(names, cashes)
            ]
        )

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
