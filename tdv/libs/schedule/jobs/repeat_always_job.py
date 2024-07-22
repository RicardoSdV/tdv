from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *
    from datetime import timedelta

    from . import DoOnceJob, RepeatUntilJob, DoReSchedule

    from ..tasks import Task

    OtherJob = Union[DoOnceJob, RepeatUntilJob]
    NextRunAt = datetime


class RepeatAlwaysJob:
    """ Holds one or more tasks. They are repeatedly called every interval from start.

    The operation is completely coupled to Schedule since it works by returning the next run_at time
    when called. After which the same instance is rescheduled to be run at the returned time. """

    __slots__ = ('run_at', 'tasks', 'interval', 'name')

    def __init__(
            self,
            interval: 'timedelta',
            start   : 'datetime' = datetime.utcnow(),
            *tasks  : 'Task',
            name    :  str = '',
    ) -> None:
        self.run_at   = start
        self.name     = name
        self.tasks    = list(tasks)
        self.interval = interval

    def __iadd__(self, task: 'Task') -> 'RepeatAlwaysJob':
        self.tasks.append(task); return self

    def __call__(self) -> 'DoReSchedule':
        for task in self.tasks: task()
        self.run_at += self.interval
        return True

    def __isub__(self, task: 'Task') -> 'RepeatAlwaysJob':
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

    def __lt__(self, other: 'Union[RepeatAlwaysJob, OtherJob]') -> bool:
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


