from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.internal.cache_service import CacheService
from tdv.domain.internal.call_hist_service import CallHistService
from tdv.domain.internal.company_service import CompanyService
from tdv.domain.internal.contract_size_service import ContractSizeService
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.expiry_service import ExpiryService
from tdv.domain.internal.insert_time_service import InsertTimeService
from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
from tdv.domain.internal.portfolio_service import PortfolioService
from tdv.domain.internal.portfolio_share_service import PortfolioShareService
from tdv.domain.internal.put_hist_service import PutHistService
from tdv.domain.internal.share_hist_service import ShareHistService
from tdv.domain.internal.strike_service import StrikeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.account_service import AccountService
from tdv.domain.internal.yahoo_finance_service import YahooFinanceService
from tdv.domain.session.session_manager import SessionManager
from tdv.infra.database import db

from tdv.infra.repos.call_hist_repo import CallHistRepo
from tdv.infra.repos.company_repo import CompanyRepo
from tdv.infra.repos.contract_size_repo import ContractSizeRepo
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.expiry_repo import ExpiryRepo
from tdv.infra.repos.insert_time_repo import InsertTimeRepo
from tdv.infra.repos.portfolio_option_repo import PortfolioOptionRepo
from tdv.infra.repos.portfolio_repo import PortfolioRepo

from tdv.infra.repos.put_hist_repo import PutHistRepo
from tdv.infra.repos.share_hist_repo import ShareHistRepo
from tdv.infra.repos.strike_repo import StrikeRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.account_repo import AccountRepo
from tdv.infra.repos.portfolio_share_repo import PortfolioShareRepo


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

    """ Base Services """
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

    """ Composer Services """
    cache = Singleton(CacheService, db, company, exchange, ticker, call_hist, put_hist, contract_size)
    yahoo_finance = Singleton(YahooFinanceService, db, ticker, insert_time, expiry, strike)
    session_manager = Singleton(SessionManager, account)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Service.yahoo_finance, Service.cache)
