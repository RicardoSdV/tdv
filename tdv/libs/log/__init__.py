from typing import TYPE_CHECKING

from .logger import Logger
from .logger_factory import LoggerFactory

types = ('Logger', 'LoggerFactory')

if TYPE_CHECKING:

    __all__ = () + types

else:
    __all__ = types