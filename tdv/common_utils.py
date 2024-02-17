import sys
from datetime import datetime
from pathlib import Path
from typing import List, Any, Iterable

from tdv.domain.data_types import TimeStamp


def get_project_root() -> Path:
    current_dir = Path(__file__).resolve()
    while not (current_dir / 'setup.py').is_file():
        current_dir = current_dir.parent
    return current_dir


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def objs_to_names(obj_list: Iterable[Any]) -> List[str]:
    return [type(obj).__name__ for obj in obj_list]


def declare_path(path: Path) -> None:
    sys.path.append(str(path))
