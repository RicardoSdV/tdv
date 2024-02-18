import os
from enum import Enum
from typing import List, Any, Dict

from tdv.common_utils import get_project_root

PROJECT_NAME = 'tdv'
SOURCE_CODE_DIR_NAME = PROJECT_NAME
BUILD_NAME = PROJECT_NAME
BUILD_VERSION = '0.1'
CLI_ROOT_COMMAND = PROJECT_NAME
CLI_ROOT_MODULE = f'{PROJECT_NAME}.cli'
CLI_ROOT_FUNC_NAME = 'cli_root'

# Paths (all absolute)
ROOT_PATH = get_project_root()
SOURCE_PATH = ROOT_PATH / 'tdv'
LOGS_DIR_PATH = ROOT_PATH / 'bin'
STORAGE_PATH = SOURCE_PATH / 'storage'
ALEMBIC_DIR_PATH = STORAGE_PATH / 'alembic'
TESLA_EXPIRATIONS_DIR_PATH = STORAGE_PATH / 'json' / 'tesla_option_chains'


class ConvertableEnum(Enum):
    """Simplify enum handling by inheriting from this class"""
    @classmethod
    def str_to_enum(cls, item_str: str) -> 'ConvertableEnum':
        for item in cls:
            if item.value == item_str:
                return item
        raise ValueError('Invalid string representation of enum')

    @classmethod
    def to_list(cls) -> List[Any]:
        return [member.value for member in cls]

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        return {member.name: member.value for member in cls}


class DbInfo(ConvertableEnum):
    USER = os.environ.get('USER')
    NAME = 'tdvdb'
    PASSWORD = 'password'
    HOST = 'localhost'
    PORT = '5432'
    RDBMS = 'postgresql'
    DBAPI = 'psycopg2'


class MarketEvents(Enum):
    OPEN = 'market_open'
    CLOSE = 'market_close'


class ExchangeNames(ConvertableEnum):
    NYSE = 'NYSE'


class TickerNames(Enum):
    TSLA = 'TSLA'
