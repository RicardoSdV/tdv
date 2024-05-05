from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.services_external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.services_internal.cache_service import CacheService
from tdv.domain.services_internal.independent_services.account_service import AccountService
from tdv.domain.services_internal.independent_services.company_service import CompanyService
from tdv.domain.services_internal.independent_services.contract_size_service import ContractSizeService
from tdv.domain.services_internal.independent_services.exchange_service import ExchangeService
from tdv.domain.services_internal.independent_services.insert_time_service import InsertTimeService
from tdv.domain.services_internal.option_services.call_hist_service import CallHistService
from tdv.domain.services_internal.option_services.expiry_service import ExpiryService
from tdv.domain.services_internal.option_services.put_hist_service import PutHistService
from tdv.domain.services_internal.option_services.strike_service import StrikeService
from tdv.domain.services_internal.portfolio_services.portfolio_option_service import PortfolioOptionService
from tdv.domain.services_internal.portfolio_services.portfolio_service import PortfolioService
from tdv.domain.services_internal.portfolio_services.portfolio_share_service import PortfolioShareService
from tdv.domain.services_internal.ticker_services.share_hist_service import ShareHistService
from tdv.domain.services_internal.ticker_services.ticker_service import TickerService
from tdv.domain.services_internal.yahoo_finance_service import YahooFinanceService
from tdv.domain.session.session_manager import SessionManager
from tdv.infra.database import db
from tdv.infra.repos.independent_repos.account_repo import AccountRepo
from tdv.infra.repos.independent_repos.company_repo import CompanyRepo
from tdv.infra.repos.independent_repos.contract_size_repo import ContractSizeRepo
from tdv.infra.repos.independent_repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.independent_repos.insert_time_repo import InsertTimeRepo
from tdv.infra.repos.option_repos.call_hist_repo import CallHistRepo
from tdv.infra.repos.option_repos.expiry_repo import ExpiryRepo
from tdv.infra.repos.option_repos.put_hist_repo import PutHistRepo
from tdv.infra.repos.option_repos.strike_repo import StrikeRepo
from tdv.infra.repos.portfolio_repos.portfolio_option_repo import PortfolioOptionRepo
from tdv.infra.repos.portfolio_repos.portfolio_repo import PortfolioRepo
from tdv.infra.repos.portfolio_repos.portfolio_share_repo import PortfolioShareRepo
from tdv.infra.repos.ticker_repos.share_hist_repo import ShareHistRepo
from tdv.infra.repos.ticker_repos.ticker_repo import TickerRepo


class Repo(DeclarativeContainer):
    # Base Cluster
    exchange = Singleton(ExchangeRepo)
    account = Singleton(AccountRepo)
    insert_time = Singleton(InsertTimeRepo)
    contract_size = Singleton(ContractSizeRepo)

    # Companies Cluster
    company = Singleton(CompanyRepo)
    ticker = Singleton(TickerRepo)
    share_hist = Singleton(ShareHistRepo)

    # Options Cluster
    expiry = Singleton(ExpiryRepo)
    strike = Singleton(StrikeRepo)
    call_hist = Singleton(CallHistRepo)
    put_hist = Singleton(PutHistRepo)

    # Portfolio Cluster
    portfolio = Singleton(PortfolioRepo)
    portfolio_option = Singleton(PortfolioOptionRepo)
    portfolio_share = Singleton(PortfolioShareRepo)


class Service(DeclarativeContainer):
    """All services live here Services"""

    # Base Cluster
    exchange = Singleton(ExchangeService, db, Repo.exchange)
    account = Singleton(AccountService, db, Repo.account)
    contract_size = Singleton(ContractSizeService, db, Repo.contract_size)

    # Companies Cluster
    company = Singleton(CompanyService, db, Repo.company)
    ticker = Singleton(TickerService, db, Repo.ticker, exchange, company)
    share_hist = Singleton(ShareHistService, db, Repo.share_hist)

    # Options Cluster
    expiry = Singleton(ExpiryService, db, Repo.expiry)
    strike = Singleton(StrikeService, db, Repo.strike)
    call_hist = Singleton(CallHistService, db, Repo.call_hist)
    put_hist = Singleton(PutHistService, db, Repo.put_hist)
    insert_time = Singleton(InsertTimeService, db, Repo.insert_time)

    # Portfolio Cluster
    portfolio = Singleton(PortfolioService, db, Repo.portfolio)
    portfolio_option = Singleton(PortfolioOptionService, db, Repo.portfolio_option)
    portfolio_share = Singleton(PortfolioShareService, db, Repo.portfolio_share)

    # Higher level Custer
    cache = Singleton(CacheService, db, company, exchange, ticker, call_hist, put_hist, contract_size)
    yahoo_finance = Singleton(YahooFinanceService, db, cache, ticker, insert_time, expiry, strike)
    session_manager = Singleton(SessionManager, account)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Service.yahoo_finance, Service.cache)
