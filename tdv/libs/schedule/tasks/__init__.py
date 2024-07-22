from typing import TYPE_CHECKING
from .task_no_args import TaskNoArgs
from .task_with_args import TaskWithArgs

types = ('TaskNoArgs', 'TaskWithArgs')

if TYPE_CHECKING:
    from typing import *

    Task = Union[TaskWithArgs, TaskNoArgs]
    Tasks = List[Task]
    Handler = Callable[..., None]
    TaskName = str

    __all__ = types + ('Task', 'Tasks', 'Handler', 'TaskName')

else:
    __all__ = types
