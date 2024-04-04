from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.option_chain_service import OptionChainsService
from tdv.domain.internal.option_service import OptionsService
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.user_service import UsersService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.option_chains_repo import OptionChainsRepo
from tdv.infra.repos.options_repo import OptionsRepo
from tdv.infra.repos.share_type_repo import ShareTypeRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.user_repo import UserRepo


class Repos(DeclarativeContainer):
    exchange_repo = Singleton(ExchangeRepo)
    ticker_repo = Singleton(TickerRepo)
    option_chains_repo = Singleton(OptionChainsRepo)
    options_repo = Singleton(OptionsRepo)
    user_repo = Singleton(UserRepo)
    share_type_repo = Singleton(ShareTypeRepo)


class InternalServices(DeclarativeContainer):
    exchange_service = Singleton(ExchangeService, db=db, exchange_repo=Repos.exchange_repo)
    ticker_service = Singleton(TickerService, db=db, ticker_repo=Repos.ticker_repo, exchange_service=exchange_service)
    option_chains_service = Singleton(OptionChainsService, db=db, option_chains_repo=Repos.option_chains_repo)
    options_service = Singleton(OptionsService, db=db, options_repo=Repos.options_repo)
    share_type_service = Singleton(ShareTypeService, db=db, share_type_repo=Repos.share_type_repo, ticker_service=ticker_service)
    users_service = Singleton(UsersService, db=db, users_repo=Repos.user_repo)


class ExternalServices(DeclarativeContainer):
    pass
