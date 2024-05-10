import os
from enum import Enum
from pathlib import Path
from typing import Dict, Tuple, Any, List, Final

MAIN_LOOP_SLEEP_TIME: Final[int] = 1
UPDATE_OPTIONS_INTERVAL: Final[int] = 5


class PROJECT:
    NAME: Final[str] = 'tdv'
    SOURCE_DIR_NAME: Final[str] = NAME


class BUILD:
    NAME: Final[str] = PROJECT.NAME
    VERSION: Final[str] = '0.1'


class PATH:
    class DIR:
        SOURCE: Final[Path] = Path(__file__).resolve().parent
        ROOT: Final[Path] = SOURCE.parent
        LOGS: Final[Path] = ROOT / 'bin'
        INFRA: Final[Path] = SOURCE / 'infra'
        DATABASE: Final[Path] = INFRA / 'database'
        ALEMBIC: Final[Path] = DATABASE / 'alembic'


class CLI:
    ROOT_COMMAND: Final[str] = PROJECT.NAME
    DIR_NAME: Final[str] = 'cli'
    ROOT_FUNC_NAME: Final[str] = 'cli_root'
    ROOT_FUNC_DOT_PATH: Final[str] = f'{PROJECT.SOURCE_DIR_NAME}.{DIR_NAME}:{ROOT_FUNC_NAME}'
    CONSOLE_ENTRY: Final[str] = f'{ROOT_COMMAND} = {ROOT_FUNC_DOT_PATH}'


class LOCAL_USER:
    NAME = 'local_user'
    EMAIL = 'local@local.local'
    PASSWORD = 'password'


class DB_INFO:
    USER = os.environ.get('USER')
    NAME = 'tdvdb'
    PASSWORD = 'password'
    HOST = 'localhost'
    PORT = '5432'
    RDBMS = 'postgresql'
    DBAPI = 'psycopg2'
    URL = f'{RDBMS}://{USER}:{PASSWORD}@{HOST}/{NAME}'


class EntityEnum(Enum):
    """Simplify enum handling by inheriting from this class"""

    @classmethod
    def validate_value(cls, value: Any) -> None:
        assert value in cls._value2member_map_

    @classmethod
    def to_list(cls) -> List[Any]:
        return [member.value for member in cls]


class COMPANY:
    class NAME(EntityEnum):
        TSLA = 'Tesla'

    class LONG_NAME(EntityEnum):
        TSLA = 'Tesla Inc.'


class CONTRACT_SIZE(EntityEnum):
    REGULAR = 100


class EXCHANGE:
    class NAME(EntityEnum):
        NEW_YORK = 'NYSE'

    class LONG_NAME(EntityEnum):
        NEW_YORK = 'New York Stock Exchange'


class CURRENCY(EntityEnum):
    US_DOLLAR = 'USD'


class TICKER(EntityEnum):
    TSLA = 'TSLA'


# Defines the relationship between exchanges, tickers & companies for fast insertion
TICKERS_BY_COMPANY_EXCHANGE: Dict[EXCHANGE.NAME, Dict[COMPANY.LONG_NAME, Tuple[TICKER, ...]]] = {
    EXCHANGE.NAME.NEW_YORK: {
        COMPANY.LONG_NAME.TSLA: (
            TICKER.TSLA,
        ),
    }
}

