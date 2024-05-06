from datetime import datetime
from json import dumps
from typing import Any


def dashed_str_YMDHMS_utcnow() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')


def datetime_from_dashed_YMD_str(dashed_YMD_str: str) -> datetime:
    return datetime.strptime(dashed_YMD_str, '%Y-%m-%d')


def turn_to_str(_any: str) -> str:
    return str(_any)


def pretty_print(data: Any) -> None:
    print(dumps(data, default=turn_to_str, indent=4))



