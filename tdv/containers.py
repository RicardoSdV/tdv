from typing import TypeVar, Callable, Type, Tuple, Dict, ClassVar, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from tdv.domain.internal.exchange_service import ExchangeService
from tdv.domain.internal.option_chain_service import OptionChainsService
from tdv.domain.internal.option_service import OptionsService
from tdv.domain.internal.share_type_service import ShareTypeService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.internal.user_options_service import UserOptionsService
from tdv.domain.internal.user_service import UsersService
from tdv.domain.internal.user_shares_service import UserSharesService
from tdv.infra.database import db
from tdv.infra.repos.exchange_repo import ExchangeRepo
from tdv.infra.repos.option_chains_repo import OptionChainsRepo
from tdv.infra.repos.options_repo import OptionsRepo
from tdv.infra.repos.share_type_repo import ShareTypeRepo
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.infra.repos.user_options_repo import UserOptionsRepo
from tdv.infra.repos.user_repo import UserRepo
from tdv.infra.repos.user_shares_repo import UserSharesRepo

# C = ClassVar[TypeFactory]

# Used to make mypy understand that this will be an object of the type created e.g. ExchangeRepo
T = TypeVar('T')  # Type
TypeFactory = Callable[..., T]  # Type Factory


def singleton(class_type: Type[T], *args: Any, **kwargs: Any) -> TypeFactory[T]:
    return Singleton(class_type, *args, **kwargs)


class Repos(DeclarativeContainer):
    exchange: ClassVar[TypeFactory[ExchangeRepo]] = Singleton(ExchangeRepo)
    ticker: ClassVar[TypeFactory[TickerRepo]] = Singleton(TickerRepo)
    option_chains: ClassVar[TypeFactory[OptionChainsRepo]] = Singleton(OptionChainsRepo)
    options: ClassVar[TypeFactory[OptionsRepo]] = Singleton(OptionsRepo)
    user: ClassVar[TypeFactory[UserRepo]] = Singleton(UserRepo)
    share_type: ClassVar[TypeFactory[ShareTypeRepo]] = Singleton(ShareTypeRepo)
    user_shares: ClassVar[TypeFactory[UserSharesRepo]] = Singleton(UserSharesRepo)
    user_options: ClassVar[TypeFactory[UserOptionsRepo]] = Singleton(UserOptionsRepo)


class Services(DeclarativeContainer):
    exchange: ClassVar[TypeFactory[ExchangeService]] = Singleton(ExchangeService, db, Repos.exchange)
    ticker = Singleton(TickerService, db, Repos.ticker, exchange)
    # ticker = singleton(TickerService, db, Repos.ticker, exchange)
    option_chains: ClassVar[TypeFactory[OptionChainsService]] = Singleton(OptionChainsService, db, Repos.option_chains)
    options: ClassVar[TypeFactory[OptionsService]] = Singleton(OptionsService, db, Repos.options)
    share_type: ClassVar[TypeFactory[ShareTypeService]] = Singleton(ShareTypeService, db, Repos.share_type, ticker)
    users: ClassVar[TypeFactory[UsersService]] = Singleton(UsersService, db, Repos.user)
    user_shares: ClassVar[TypeFactory[UserSharesService]] = Singleton(UserSharesService, db, Repos.user_shares, ticker,
                                                                      share_type)
    user_options: ClassVar[TypeFactory[UserOptionsService]] = Singleton(UserOptionsService, db, Repos.user_options)


class ExternalServices(DeclarativeContainer):
    pass
