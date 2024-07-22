from datetime import datetime
from json import dumps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    DashedStrStampYMDHMS = str
    DashedStrStampYMD = str


def datetime_from_dashed_YMD_str(_str: 'DashedStrStampYMD') -> datetime:
    return datetime.strptime(_str, '%Y-%m-%d')


def pretty_print(data: 'Any') -> None:
    print(dumps(data, default=lambda x: str(x), indent=4))
