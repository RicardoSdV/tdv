from inspect import ismethod
from typing import Optional

from tdv.domain.types import Args, Handler, KwArgs


class Task:
    """Class that holds a Callable and optionally its args and kwargs for calling at a later point in time"""
    __slots__ = ('__handler', '__args', '__kwargs')

    def __init__(self, handler: Handler, args: Optional[Args] = None, kwargs: Optional[KwArgs] = None) -> None:
        self.__handler: Handler = handler
        self.__args: Optional[Args] = args
        self.__kwargs: Optional[KwArgs] = kwargs

    def __call__(self) -> None:
        self.__handler(*(self.__args or ()), **(self.__kwargs or {}))

    def __repr__(self) -> str:
        if ismethod(self.__handler):
            return f'handler = {self.__handler.__name__}.{self.__handler.__self__.__class__.__name__}'
        else:
            return f'handler = {self.__handler.__name__}'
