from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.cache.cache_manager import CacheManager
from tdv.domain.cache.entity_cache import EntityCache
from tdv.domain.services.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.services.independent_services.account_service import AccountService
from tdv.domain.services.independent_services.company_service import CompanyService
from tdv.domain.services.independent_services.contract_size_service import ContractSizeService
from tdv.domain.services.independent_services.exchange_service import ExchangeService
from tdv.domain.services.independent_services.insert_time_service import InsertTimeService
from tdv.domain.services.option_services.expiry_service import ExpiryService
from tdv.domain.services.option_services.option_hist_service import OptionHistService
from tdv.domain.services.option_services.strike_service import StrikeService
from tdv.domain.services.portfolio_services.portfolio_option_service import PortfolioOptionService
from tdv.domain.services.portfolio_services.portfolio_service import PortfolioService
from tdv.domain.services.portfolio_services.portfolio_share_service import PortfolioShareService
from tdv.domain.services.ticker_services.share_hist_service import ShareHistService
from tdv.domain.services.ticker_services.ticker_service import TickerService
from tdv.domain.services.yahoo_finance_service import YahooFinanceService
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


class Cache(DeclarativeContainer):
    entity = Singleton(EntityCache)


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
    exchange = Singleton(ExchangeService, db, Cache.entity, Repo.exchange)
    account = Singleton(AccountService, db, Repo.account)
    contract_size = Singleton(ContractSizeService, Cache.entity, Repo.contract_size)

    # Companies Cluster
    company = Singleton(CompanyService, Cache.entity, Repo.company)
    ticker = Singleton(TickerService, Cache.entity, Repo.ticker, exchange, company)
    share_hist = Singleton(ShareHistService, Repo.share_hist)

    # Options Cluster
    expiry = Singleton(ExpiryService, Repo.expiry)
    strike = Singleton(StrikeService, Repo.strike)
    option_hist = Singleton(OptionHistService, Repo.call_hist, Repo.put_hist)
    insert_time = Singleton(InsertTimeService, Repo.insert_time)

    # Portfolio Cluster
    portfolio_option = Singleton(PortfolioOptionService, Cache.entity, Repo.portfolio_option, expiry, strike)
    portfolio_share = Singleton(PortfolioShareService, Cache.entity, Repo.portfolio_share)
    portfolio = Singleton(PortfolioService, Cache.entity, Repo.portfolio, portfolio_share, portfolio_option)

    yahoo_finance = Singleton(
        YahooFinanceService, db, Cache.entity, ticker, expiry, strike, insert_time, share_hist, option_hist
    )
    session_manager = Singleton(SessionManager, account)

    cache_manager = Singleton(CacheManager, db, Cache.entity, exchange, ticker, company, contract_size)


class ExternalService(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Service.yahoo_finance, Cache.entity)
