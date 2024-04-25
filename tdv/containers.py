from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.internal.company_service import CompanyService
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
from tdv.domain.internal.portfolio_service import PortfolioService
from tdv.domain.internal.session_service import SessionService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.account_service import AccountService
from tdv.domain.internal.yahoo_finance_service import YahooFinanceService
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


class Repos(DeclarativeContainer):
    account = Singleton(AccountRepo)
    call_hist = Singleton(CallHistRepo)
    company = Singleton(CompanyRepo)
    contract_size = Singleton(ContractSizeRepo)
    exchange = Singleton(ExchangeRepo)
    expiry = Singleton(ExpiryRepo)
    insert_time = Singleton(InsertTimeRepo)
    portfolio_option = Singleton(PortfolioOptionRepo)
    portfolio = Singleton(PortfolioRepo)
    portfolio_share = Singleton(PortfolioShareRepo)
    put_hist = Singleton(PutHistRepo)
    share_hist = Singleton(ShareHistRepo)
    strike = Singleton(StrikeRepo)
    ticker = Singleton(TickerRepo)



class Services(DeclarativeContainer):
    exchange = Singleton(ExchangeService, db, Repos.exchange)
    ticker = Singleton(TickerService, db, Repos.ticker, exchange)
    account = Singleton(AccountService, db, Repos.user)
    # portfolio_share = Singleton(PortfolioShareService, db, Repos.portfolio_share, ticker, share_type)
    portfolio_option = Singleton(PortfolioOptionService, db, Repos.portfolio_option)
    portfolio = Singleton(PortfolioService, db, Repos.portfolio)
    yahoo_finance = Singleton(YahooFinanceService, db, ticker)
    session = Singleton(SessionService, account)
    company = Singleton(CompanyService, Repos.comany)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Services.yahoo_finance)
