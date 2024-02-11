from typing import List, Callable, Self


class Event:
    def __init__(self) -> None:
        self.__handlers: List[Callable] = []

    def __iadd__(self, handler: Callable) -> Self:
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler: Callable) -> Self:
        self.__handlers.remove(handler)
        return self

    def __call__(self, *args, **kwargs) -> None:
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Event({self.__class__.__name__})({len(self.__handlers)}):{repr(self.__handlers)}"

    def clear(self) -> None:
        self.__handlers: List[Callable] = []
