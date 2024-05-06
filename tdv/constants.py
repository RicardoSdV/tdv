import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Tuple, Any, List

# Paths (all absolute)
SOURCE_DIR_PATH = Path(__file__).resolve().parent
ROOT_DIR_PATH = SOURCE_DIR_PATH.parent
LOGS_DIR_PATH = ROOT_DIR_PATH / 'bin'
INFRA_DIR_PATH = SOURCE_DIR_PATH / 'infra'
DATABASE_DIR_PATH = INFRA_DIR_PATH / 'database'
ALEMBIC_DIR_PATH = DATABASE_DIR_PATH / 'alembic'
ALEMBIC_INI_PATH = ALEMBIC_DIR_PATH / 'alembic.ini'

# Naming
PROJECT_NAME = 'tdv'
SOURCE_CODE_DIR_NAME = PROJECT_NAME
BUILD_NAME = PROJECT_NAME
BUILD_VERSION = '0.1'
CLI_ROOT_COMMAND = PROJECT_NAME
CLI_ROOT_MODULE = f'{PROJECT_NAME}.cli'
CLI_ROOT_FUNC_NAME = 'cli_root'

MAIN_LOOP_SLEEP_TIME = 1
UPDATE_OPTIONS_INTERVAL = 5


@dataclass
class LocalAccountInfo:
    username = 'local_user'
    email = 'local@local.local'
    password = 'password'
    session_id = 'local_session_id'


class DbInfo(Enum):
    USER = os.environ.get('USER')
    NAME = 'tdvdb'
    PASSWORD = 'password'
    HOST = 'localhost'
    PORT = '5432'
    RDBMS = 'postgresql'
    DBAPI = 'psycopg2'

    @classmethod
    def make_sqlalchemy_url(cls) -> str:
        return f'{cls.RDBMS.value}://{cls.USER.value}:{cls.PASSWORD.value}@{cls.HOST.value}/{cls.NAME.value}'


class MarketEvents(Enum):
    OPEN = 'market_open'
    CLOSE = 'market_close'


class EntityEnum(Enum):
    """Simplify enum handling by inheriting from this class"""

    @classmethod
    def validate_value(cls, value: Any) -> None:
        assert value in cls._value2member_map_

    @classmethod
    def to_list(cls) -> List[Any]:
        return [member.value for member in cls]


@dataclass
class Companies:
    class ShortNames(EntityEnum):
        TSLA = 'Tesla'

    class LongNames(EntityEnum):
        TSLA = 'Tesla Inc.'


class ContractSizes(EntityEnum):
    REGULAR = 100


@dataclass
class Exchanges:
    class ShortNames(EntityEnum):
        NEW_YORK = 'NYSE'

    class LongNames(EntityEnum):
        NEW_YORK = 'New York Stock Exchange'


class Currencies(EntityEnum):
    US_DOLLAR = 'USD'


class Tickers(EntityEnum):
    TSLA = 'TSLA'


# Defines the relationship between exchanges, tickers & companies for fast insertion
TICKERS_BY_COMPANY_EXCHANGE: Dict[Exchanges.ShortNames, Dict[Companies.LongNames, Tuple[Tickers, ...]]] = {
    Exchanges.ShortNames.NEW_YORK: {
        Companies.LongNames.TESLA: (Tickers.TSLA,),
    }
}
