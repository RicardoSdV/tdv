from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.internal import ExchangesService, TickerService, OptionChainsService, OptionsService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.option_chains_repo import OptionChainsRepo
from tdv.infra.repos.options_repo import OptionsRepo
from tdv.infra.repos.ticker_repo import TickerRepo


class Repos(DeclarativeContainer):
    exchange_repo = Singleton(ExchangeRepo)
    ticker_repo = Singleton(TickerRepo)
    option_chains_repo = Singleton(OptionChainsRepo)
    options_repo = Singleton(OptionsRepo)


class InternalServices(DeclarativeContainer):
    exchange_service = Singleton(ExchangesService, db=db, exchange_repo=Repos.exchange_repo)
    ticker_service = Singleton(TickerService, db=db, ticker_repo=Repos.ticker_repo)
    option_chains_service = Singleton(OptionChainsService, db=db, option_chains_repo=Repos.option_chains_repo)
    options_service = Singleton(OptionsService, db=db, options_repo=Repos.options_repo)


class ExternalServices(DeclarativeContainer):
    pass
