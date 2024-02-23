from json import dump
from pathlib import Path
from typing import Any, Optional, Callable

from tdv.common_utils import timestamp_str


class BaseSerializer:
    @staticmethod
    def _turn_to_str(_any: str) -> str:
        return str(_any)


class BasePathBuilder:
    @staticmethod
    def _get_timestamp_path(dir_path: Path) -> Path:
        return (dir_path / timestamp_str()).with_suffix('.json')


class BaseRepo:
    @staticmethod
    def _save_to_json(
            path: Path,
            data: Any,
            default_serializer: Optional[Callable] = None,
            indent: Optional[int] = None,
    ) -> None:
        with open(path, 'w') as json_file:
            dump(data, json_file, default=default_serializer, skipkeys=True, indent=indent)
