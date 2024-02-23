import sys
from datetime import datetime
from pathlib import Path

from tdv.constants import ALEMBIC_INI_PATH
from tdv.domain.types import TimeStamp


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def declare_path(path: Path) -> None:
    sys.path.append(str(path))
