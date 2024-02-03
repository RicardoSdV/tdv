from datetime import datetime, timezone

from tdv.types import TimeStamp


def now_timestamp(cls) -> datetime:
    return datetime.now()


def timestamp_str() -> TimeStamp:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


