from typing import List, TYPE_CHECKING


from sqlalchemy import Connection

from local_user_data.portfolio_data import local_user_portfolio_data
from tdv.domain.entities.independent_entities.account_entity import Account
from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.portfolio_repos.portfolio_repo import PortfolioRepo
    from tdv.domain.services_internal.cache_service import CacheService
    from tdv.domain.services_internal.portfolio_services.portfolio_share_service import PortfolioShareService
    from tdv.domain.services_internal.portfolio_services.portfolio_option_service import PortfolioOptionService

logger = LoggerFactory.make_logger(__name__)


class PortfolioService:
    def __init__(self, db: 'DB', portfolio_repo: 'PortfolioRepo', cache_service: 'CacheService', pfol_share_service: 'PortfolioShareService', pfol_option_service: 'PortfolioOptionService') -> None:
        self.__db = db
        self.__portfolio_repo = portfolio_repo
        self.__cache_service = cache_service
        self.__pfol_share_service = pfol_share_service
        self.__pfol_option_service = pfol_option_service


    def create_all_local_user_portfolios(self, account: Account, conn: Connection) -> List[Portfolio]:
        for name, data in local_user_portfolio_data.items():
            cash, shares_data, options_data = data['cash'], data['shares'], data['option_data']

            portfolio = Portfolio(account_id=account.id, name=name, cash=cash)

            with self.__db.connect as conn:

                portfolio = self.__portfolio_repo.insert(conn, [portfolio])[0]

                for ticker_name, count in shares_data.items():
                    tickers_by_id = self.__cache_service.tickers_by_id

                    for t in tickers_by_id.values():
                        if t.name == ticker_name:
                            ticker = t
                            break
                    else:
                        ticker = None

                    pfol_share = self.__pfol_share_service.create_portfolio_share(ticker, count, conn)

                    self.__pfol_option_service.create_portfolio_options(conn)

                    # buscar en el DB un ticker
















            for option_data in options_data:
                count, expiry_date, strike_price, ticker_name = option_data['count'], option_data['expiry_date'], option_data['strike'], option_data['ticker']




        portfolios = Service.portfolio().create_many_portfolios(account_id, names, cashes, conn)

        # portfolio shares
        portfolio_ids = [portfolio.id for portfolio in portfolios]
        Service.portfolio_share().create_many_portfolio_shares(portfolio_ids, ticker_id, counts, conn)

        # portfolio options
        Service.portfolio_option().create_many_portfolio_options(portfolio_ids, options, conn)

        conn.commit()

    def create_portfolio(self, account_id: int, portfolio_name: str) -> List[Portfolio]:
        logger.debug('Creating portfolio', account_id=account_id, portfolio_name=portfolio_name)
        portfolios = [Portfolio(account_id=account_id, name=portfolio_name)]

        with self.__db.connect as conn:
            result = self.__portfolio_repo.insert(conn, portfolios)
            conn.commit()
        return result

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
