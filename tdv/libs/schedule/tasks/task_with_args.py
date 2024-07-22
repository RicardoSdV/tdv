from inspect import ismethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    from . import Handler


class TaskWithArgs:
    """ Holds Callable (Handler) & optionally its args & kwargs for calling later.
    A logger_name can be given to the task, else it will default to the Handlers' logger_name

    DANGER: Do bear in mind that if such a task is held in a repeating job & the held args
    or kwargs are mutable data structures (e.g. lists, dicts, objects such as entities, etc.)
    & such structures are mutated during the call of the Handler this mutation will remain in the
    next call of this handler. This is the intended operation, deep copy too expensive. """

    __slots__ = ('handler', 'name', 'args', 'kwargs')

    def __init__(
            self,
            handler:  'Handler',
            name:     'Optional[str]' = None,
            *args:    'Any',
            **kwargs: 'Any'
    ) -> None:
        self.name    = handler.__name__ if name is None else name
        self.handler = handler
        self.args    = args
        self.kwargs  = kwargs

    def __call__(self) -> None:
        self.handler(*(self.args or ()), **(self.kwargs or {}))

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(self.task_name={self.name}, self.handler.__name__={self.handler.__name__}), '
                f'self.args={self.args}, self.kwargs={self.kwargs}')
