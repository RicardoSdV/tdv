# Monkey-patch gunicorn before anything
import gevent.monkey

gevent.monkey.patch_all()

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.api.gunicorn_http_server import GunicornHTTPServer
from tdv.api.resources.ping_resource import PingResource
from tdv.api.falcon_app import FalconApp
from tdv.api.resources.test_render import TestRender
from tdv.constants import PATH
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
from tdv.libs.log import LoggerFactory


logger_factory = LoggerFactory(logs_dir_path=PATH.DIR.LOGS)


class Cache(DeclarativeContainer):
    entity = Singleton(EntityCache)


class Repo(DeclarativeContainer):

    data_gather_logger = logger_factory.make_logger('data_gather_repos')

    # Base Cluster
    exchange      = Singleton(ExchangeRepo,     data_gather_logger)
    account       = Singleton(AccountRepo,      data_gather_logger)
    insert_time   = Singleton(InsertTimeRepo,   data_gather_logger)
    contract_size = Singleton(ContractSizeRepo, data_gather_logger)

    # Companies Cluster
    company = Singleton(CompanyRepo,      data_gather_logger)
    ticker = Singleton(TickerRepo,        data_gather_logger)
    share_hist = Singleton(ShareHistRepo, data_gather_logger)

    # Options Cluster
    expiry = Singleton(ExpiryRepo,      data_gather_logger)
    strike = Singleton(StrikeRepo,      data_gather_logger)
    call_hist = Singleton(CallHistRepo, data_gather_logger)
    put_hist = Singleton(PutHistRepo,   data_gather_logger)

    # Portfolio Cluster
    user_data_logger = logger_factory.make_logger('user_data_repos')
    portfolio        = Singleton(PortfolioRepo,       user_data_logger)
    portfolio_option = Singleton(PortfolioOptionRepo, user_data_logger)
    portfolio_share  = Singleton(PortfolioShareRepo,  user_data_logger)


class Service(DeclarativeContainer):
    data_gather_logger = logger_factory.make_logger('data_gather_services')

    # Base Cluster
    exchange      = Singleton(ExchangeService, db, Cache.entity, Repo.exchange, data_gather_logger)
    account       = Singleton(AccountService,  db, Repo.account, data_gather_logger)
    contract_size = Singleton(ContractSizeService, Cache.entity, Repo.contract_size, data_gather_logger)

    # Companies Cluster
    company    = Singleton(CompanyService, Cache.entity, Repo.company, data_gather_logger)
    ticker     = Singleton(TickerService, Cache.entity, Repo.ticker, exchange, company, data_gather_logger)
    share_hist = Singleton(ShareHistService, Repo.share_hist, data_gather_logger)

    # Options Cluster
    expiry = Singleton(ExpiryService, Repo.expiry, data_gather_logger)
    strike = Singleton(StrikeService, Repo.strike, data_gather_logger)
    option_hist = Singleton(OptionHistService, Repo.call_hist, Repo.put_hist, data_gather_logger)
    insert_time = Singleton(InsertTimeService, Repo.insert_time, data_gather_logger)

    yahoo_finance = Singleton(
        YahooFinanceService, db, Cache.entity, ticker, expiry, strike, insert_time, share_hist, option_hist, data_gather_logger
    )

    # Portfolio Cluster
    user_data_logger = logger_factory.make_logger('user_data_services')
    portfolio_option = Singleton(PortfolioOptionService, Cache.entity, Repo.portfolio_option, expiry, strike, user_data_logger)
    portfolio_share = Singleton(PortfolioShareService, Cache.entity, Repo.portfolio_share, user_data_logger)
    portfolio = Singleton(PortfolioService, Repo.portfolio, portfolio_share, portfolio_option, user_data_logger)

    session_manager = Singleton(
        SessionManager, db, Cache.entity, account, portfolio, portfolio_share, portfolio_option, strike, expiry,
        logger_factory.make_logger('session_manager')
    )

    cache_manager = Singleton(CacheManager, db, Cache.entity, exchange, ticker, company, contract_size)


class ExternalService(DeclarativeContainer):
    yahoo_finance = Singleton(
        YahooFinanceServiceProxy, Service.yahoo_finance, Cache.entity, logger_factory.make_logger('yf_service_proxy')
    )


class API(DeclarativeContainer):
    logger = logger_factory.make_logger('api')

    ping = Singleton(PingResource)
    test_render = Singleton(TestRender)

    falcon_app = Singleton(FalconApp, (ping(), test_render()), logger=logger)
    gunicorn_server = Singleton(GunicornHTTPServer, falcon_app, logger)
