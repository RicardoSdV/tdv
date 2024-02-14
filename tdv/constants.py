from enum import Enum

from tdv.common_utils import get_project_root

# Paths (all absolute)
ROOT_PATH = get_project_root()
SOURCE_PATH = ROOT_PATH / 'tdv'
TESLA_EXPIRATIONS_DIR_PATH = SOURCE_PATH / 'storage' / 'json' / 'tesla_option_chains'
LOGS_DIR_PATH = ROOT_PATH / 'bin'


class MarketEvent(Enum):
    OPEN = 'market_open'
    CLOSE = 'market_close'
