import sys
from datetime import datetime
from json import dumps
from pathlib import Path
from typing import Any

from tdv.domain.types import TimeStamp


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def str_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, '%Y-%m-%d')



def _turn_to_str(_any: str) -> str:
    return str(_any)


def pretty_print(data: Any):
    print(dumps(data, default=_turn_to_str, indent=4))