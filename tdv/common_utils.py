from datetime import datetime

from tdv.types import TimeStamp


def timestamp() -> TimeStamp:
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")