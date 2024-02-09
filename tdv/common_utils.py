from datetime import datetime, timezone
from pathlib import Path

from tdv.data_types import TimeStamp


def get_project_root() -> Path:
    current_dir = Path(__file__).resolve()
    while not (current_dir / 'setup.py').is_file():
        current_dir = current_dir.parent
    return current_dir


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


