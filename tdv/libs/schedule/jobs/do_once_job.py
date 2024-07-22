from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *
    from datetime import datetime

    from . import RepeatUntilJob, RepeatAlwaysJob

    from ..tasks import Task

    OtherJob = Union[RepeatUntilJob, RepeatAlwaysJob]


class DoOnceJob:
    """ Holds & calls one or more tasks at a point in time then is destroyed """

    __slots__ = ('run_at', 'tasks', 'name')

    def __init__(self, run_at: 'datetime', name: str = '', *tasks: 'Task') -> None:
        self.name   = name
        self.run_at = run_at
        self.tasks  = list(tasks)

    def __iadd__(self, task: 'Task') -> 'DoOnceJob':
        self.tasks.append(task)
        return self

    def __call__(self) -> None:
        for task in self.tasks: task()

    def __isub__(self, task: 'Task') -> 'DoOnceJob':
        self.tasks.remove(task); return self

    def remove_tasks(self, task_name: str) -> None:
        i = 0
        tasks = self.tasks
        while i < len(tasks):
            if tasks[i].name == task_name:
                del tasks[i]
            else:
                i += 1

    def __contains__(self, task_name: str) -> bool:
        for task in self.tasks:
            if task.name == task_name:
                return True
        return False

    def __lt__(self, other: 'Union[DoOnceJob, OtherJob]') -> bool:
        return self.run_at < other.run_at  # Needed for the operation of insort

    def __len__(self) -> int: return len(self.tasks)

    def __repr__(self) -> str:
        bundles_repr = ',\n        '.join(repr(task) for task in self.tasks)
        return (f'{self.__class__.__name__}(\n'
                f'    trigger_at = {self.run_at},\n'
                f'    handler_bundles = [\n'
                f'        {bundles_repr}\n'
                f'    ]\n'
                f')')
