import os
from enum import Enum
from pathlib import Path


from tdv.domain.entities.exchange_entity import Exchanges
from tdv.domain.entities.ticker_entity import Tickers, Companies

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


TICKERS_BY_EXCHANGE = {  # All tickers by exchange that exist for this program should be here
    Exchanges.NEW_YORK.value: [Tickers.TSLA.value],
}

TICKERS_BY_COMPANY = {
    Companies.TSLA.value: [Tickers.TSLA.value],
}
