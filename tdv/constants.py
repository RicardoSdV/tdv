import os
from enum import Enum

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


class DbInfo(Enum):
    USER = os.environ.get('USER')
    NAME = 'tdvdb'
    PASSWORD = 'password'
    HOST = 'localhost'


class MarketEvents(Enum):
    OPEN = 'market_open'
    CLOSE = 'market_close'


class Exchanges(Enum):
    NYSE = 'NYSE'


class Tickers(Enum):
    TSLA = 'TSLA'
