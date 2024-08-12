from typing import TYPE_CHECKING

from .. import Task

if TYPE_CHECKING:
    from typing import *


class TaskWithArgs(Task):
    """ Holds Callable (Handler) & optionally its args & kwargs for calling later.
    A logger_name can be given to the task, else it will default to the Handlers' logger_name

    DANGER: Do bear in mind that if such a task is held in a repeating job & the held args
    or kwargs are mutable data structures (e.g. lists, dicts, objects such as entities, etc.)
    & such structures are mutated during the call of the Handler this mutation will remain in the
    next call of this handler. This is the intended operation, deep copy too expensive. """

    __slots__ = ('args', 'kwargs')

    def __init__(
            self,
            handler:  'Callable',
            name:     'Optional[str]' = None,
            *args:    'Any',
            **kwargs: 'Any'
    ) -> None:
        super().__init__(handler, name)
        self.args   = args
        self.kwargs = kwargs

    def __call__(self) -> None:
        self.handler(*(self.args or ()), **(self.kwargs or {}))

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(self.task_name={self.name}, self.handler.__name__={self.handler.__name__}), '
                f'self.args={self.args}, self.kwargs={self.kwargs}')
