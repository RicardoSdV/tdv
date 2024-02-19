import os
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


def config_parser() -> None:
    import configparser
    from tdv.constants import DbInfo

    config = configparser.ConfigParser()

    path = 'tdv/storage/alembic/alembic.ini'  # TODO: make Path()

    config.optionxform = str  # Preserve case sensitivity
    config.read(path)

    i = DbInfo.to_dict()
    sqlalchemy_url = f"{i['RDBMS']}://{i['USER']}:{i['PASSWORD']}@{i['HOST']}/{i['NAME']}"

    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if line.startswith('sqlalchemy.url'):
                f.write(f'sqlalchemy.url = {sqlalchemy_url}\n')
            else:
                f.write(line)
