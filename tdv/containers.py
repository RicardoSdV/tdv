from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.option_chain_service import OptionChainsService
from tdv.domain.internal.option_service import OptionsService
from tdv.domain.internal.portfolio_options_service import PortfolioOptionsService
from tdv.domain.internal.portfolios_service import PortfoliosService
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.user_service import UsersService
from tdv.domain.internal.portfolio_shares_service import PortfolioSharesService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.option_chains_repo import OptionChainsRepo
from tdv.infra.repos.options_repo import OptionsRepo
from tdv.infra.repos.portfolio_options_repo import PortfolioOptionsRepo
from tdv.infra.repos.portfolios_repo import PortfoliosRepo
from tdv.infra.repos.share_type_repo import ShareTypeRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.user_repo import UserRepo
from tdv.infra.repos.portfolio_shares_repo import PortfolioSharesRepo


class Repos(DeclarativeContainer):
    exchange = Singleton(ExchangeRepo)
    ticker = Singleton(TickerRepo)
    option_chains = Singleton(OptionChainsRepo)
    options = Singleton(OptionsRepo)
    user = Singleton(UserRepo)
    share_type = Singleton(ShareTypeRepo)
    portfolio_shares = Singleton(PortfolioSharesRepo)
    portfolio_options = Singleton(PortfolioOptionsRepo)
    portfolios = Singleton(PortfoliosRepo)


class Services(DeclarativeContainer):
    exchange = Singleton(ExchangeService, db, Repos.exchange)
    ticker = Singleton(TickerService, db, Repos.ticker, exchange)
    option_chains = Singleton(OptionChainsService, db, Repos.option_chains)
    options = Singleton(OptionsService, db, Repos.options)
    share_type = Singleton(ShareTypeService, db, Repos.share_type, ticker)
    users = Singleton(UsersService, db, Repos.user)
    portfolio_shares = Singleton(PortfolioSharesService, db, Repos.portfolio_shares, Repos.ticker, Repos.share_type)
    portfolio_options = Singleton(PortfolioOptionsService, db, Repos.portfolio_options)
    portfolios = Singleton(PortfoliosService, db, Repos.portfolios)


class ExternalServices(DeclarativeContainer):
    pass
