from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *


class Task:
    """ Holds Callable (Handler). A task_name can be given to the task, else defaults to the Handlers' task_name """

    __slots__ = ('name', 'handler')

    def __init__(self, handler: 'Callable', name: 'Optional[str]' = None) -> None:
        # Task names held as attr because holding no names at all limits the operation of schedule, so does forcing
        # the uniqueness of the names by holding them in a dict in Job, & more... don't delete name from here!
        self.name    = handler.__name__ if name is None else name
        self.handler = handler

    def __call__(self) -> None:
        self.handler()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(self.task_name={self.name}, self.handler.__name__={self.handler.__name__})'
