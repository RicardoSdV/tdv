from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.internal.company_service import CompanyService
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
from tdv.domain.internal.portfolio_service import PortfolioService
from tdv.domain.session.session import Session
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

    exchange = Singleton(ExchangeService, db, Repo.exchange)
    company = Singleton(CompanyService, db, Repo.company)
    ticker = Singleton(TickerService, db, Repo.ticker, exchange, company)
    account = Singleton(AccountService, db, Repo.account)
    # portfolio_share = Singleton(PortfolioShareService, db, Repos.portfolio_share, ticker, share_type)
    portfolio_option = Singleton(PortfolioOptionService, db, Repo.portfolio_option)
    portfolio = Singleton(PortfolioService, db, Repo.portfolio)
    yahoo_finance = Singleton(YahooFinanceService, db, ticker)

    session_manager = Singleton(SessionManager, account)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Service.yahoo_finance)
