from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
from tdv.domain.internal.portfolio_service import PortfolioService
from tdv.domain.internal.session_service import SessionService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.account_service import AccountService
from tdv.domain.internal.yahoo_finance_service import YahooFinanceService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.portfolio_option_repo import PortfolioOptionRepo
from tdv.infra.repos.portfolio_repo import PortfolioRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.account_repo import AccountRepo
from tdv.infra.repos.portfolio_share_repo import PortfolioShareRepo


class Repos(DeclarativeContainer):
    exchange = Singleton(ExchangeRepo)
    ticker = Singleton(TickerRepo)
    account = Singleton(AccountRepo)
    portfolio_share = Singleton(PortfolioShareRepo)
    portfolio_option = Singleton(PortfolioOptionRepo)
    portfolio = Singleton(PortfolioRepo)


class Services(DeclarativeContainer):
    exchange = Singleton(ExchangeService, db, Repos.exchange)
    ticker = Singleton(TickerService, db, Repos.ticker, exchange)
    account = Singleton(AccountService, db, Repos.user)
    # portfolio_share = Singleton(PortfolioShareService, db, Repos.portfolio_share, ticker, share_type)
    portfolio_option = Singleton(PortfolioOptionService, db, Repos.portfolio_option)
    portfolio = Singleton(PortfolioService, db, Repos.portfolio)
    yahoo_finance = Singleton(YahooFinanceService, db, ticker)
    session = Singleton(SessionService, account)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Services.yahoo_finance)
