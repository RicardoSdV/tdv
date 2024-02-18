from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tdv.storage.db import DB
    from tdv.storage.exchange_repo import ExchangeRepo
    from tdv.storage.option_chains_repo import OptionChainsRepo
    from tdv.storage.options_repo import OptionsRepo
    from tdv.storage.ticker_repo import TickerRepo


class Storage:
    def __init__(self) -> None:
        self.__db: Optional['DB'] = None
        self.__exchange_repo: Optional['ExchangeRepo'] = None
        self.__ticker_repo: Optional['TickerRepo'] = None
        self.__option_chains_repo: Optional['OptionChainsRepo'] = None
        self.__options_repo: Optional['OptionsRepo'] = None

    @property
    def db(self) -> 'DB':
        if self.__db is None:
            from tdv.storage.db import DB
            self.__db = DB()
        return self.__db

    @property
    def exchange_repo(self) -> 'ExchangeRepo':
        if self.__exchange_repo is None:
            from tdv.storage.exchange_repo import ExchangeRepo
            self.__exchange_repo = ExchangeRepo()
        return self.__exchange_repo

    @property
    def ticker_repo(self) -> 'TickerRepo':
        if self.__ticker_repo is None:
            from tdv.storage.ticker_repo import TickerRepo
            self.__ticker_repo = TickerRepo()
        return self.__ticker_repo

    @property
    def option_chains_repo(self) -> 'OptionChainsRepo':
        if self.__option_chains_repo is None:
            from tdv.storage.option_chains_repo import OptionChainsRepo
            self.__option_chains_repo = OptionChainsRepo()
        return self.__option_chains_repo

    @property
    def options_repo(self) -> 'OptionsRepo':
        if self.__options_repo is not None:
            from tdv.storage.options_repo import OptionsRepo
            self.__options_repo = OptionsRepo()
        return self.__options_repo


storage = Storage()
