from datetime import datetime
from json import dumps
from typing import Any


def str_timestamp_of_now() -> str:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def str_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, '%Y-%m-%d')


def turn_to_str(_any: str) -> str:
    return str(_any)


def pretty_print(data: Any):
    print(dumps(data, default=turn_to_str, indent=4))
