from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.external.yahoo_finance_service_proxy import YahooFinanceServiceProxy
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.option_service import OptionService
from tdv.domain.internal.option_history_service import OptionHistoryService
from tdv.domain.internal.portfolio_option_service import PortfolioOptionService
from tdv.domain.internal.portfolio_service import PortfoliosService
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.account_service import AccountService
from tdv.domain.internal.portfolio_share_service import PortfolioSharesService
from tdv.domain.internal.yahoo_finance_service import YahooFinanceService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.option_history_repo import OptionHistoryRepo
from tdv.infra.repos.option_repo import OptionRepo
from tdv.infra.repos.portfolio_options_repo import PortfolioOptionsRepo
from tdv.infra.repos.portfolios_repo import PortfoliosRepo
from tdv.infra.repos.share_type_repo import ShareTypeRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.account_repo import UserRepo
from tdv.infra.repos.portfolio_shares_repo import PortfolioSharesRepo


class Repos(DeclarativeContainer):
    exchange = Singleton(ExchangeRepo)
    ticker = Singleton(TickerRepo)
    option = Singleton(OptionRepo)
    option_history = Singleton(OptionHistoryRepo)
    user = Singleton(UserRepo)
    share_type = Singleton(ShareTypeRepo)
    portfolio_share = Singleton(PortfolioSharesRepo)
    portfolio_option = Singleton(PortfolioOptionsRepo)
    portfolio = Singleton(PortfoliosRepo)


class Services(DeclarativeContainer):
    exchange = Singleton(ExchangeService, db, Repos.exchange)
    ticker = Singleton(TickerService, db, Repos.ticker, exchange)
    option_chain = Singleton(OptionService, Repos.option)
    option = Singleton(OptionHistoryService, Repos.option_history)
    share_type = Singleton(ShareTypeService, db, Repos.share_type, ticker)
    account = Singleton(AccountService, db, Repos.user)
    portfolio_share = Singleton(PortfolioSharesService, db, Repos.portfolio_share, ticker, share_type)
    portfolio_option = Singleton(PortfolioOptionService, db, Repos.portfolio_option)
    portfolio = Singleton(PortfoliosService, db, Repos.portfolio)
    yahoo_finance = Singleton(YahooFinanceService, db, ticker, option_chain, option)


class ExternalServices(DeclarativeContainer):
    yahoo_finance = Singleton(YahooFinanceServiceProxy, Services.yahoo_finance)
