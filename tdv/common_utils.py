from datetime import datetime, timezone
from pathlib import Path
from typing import List, Any

from tdv.data_types import TimeStamp


def get_project_root() -> Path:
    current_dir = Path(__file__).resolve()
    while not (current_dir / 'setup.py').is_file():
        current_dir = current_dir.parent
    return current_dir


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def turn_list_of_objects_into_list_of_names_of_their_classes(obj_list: List[Any]) -> List[str]:
    return [type(obj).__name__ for obj in obj_list]
