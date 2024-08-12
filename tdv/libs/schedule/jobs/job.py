from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    from .. import Task, Timestamp


class Job:
    __slots__ = ('name', 'run_at', 'tasks', 'add_task', 'rem_task')

    def __init__(
        self,
        run_at: 'Timestamp',
        name: str = '',
        *tasks: 'Task'
    ) -> None:
        self.name     = name
        self.run_at   = run_at
        self.tasks    = list(tasks)
        self.add_task = self.tasks.append
        self.rem_task = self.tasks.remove

    def __call__(self) -> bool:
        for task in self.tasks:
            task()
        return False

    def rem_task_by_name(self, task_name: str) -> 'Optional[Task]':
        for i, task in enumerate(self.tasks):
            if task.name == task_name:
                del self.tasks[i]
                return task
        return None

    def rem_tasks(self, task_name: str) -> None:
        i = 0
        tasks = self.tasks
        len_tasks = len(tasks)
        while i < len_tasks:
            if tasks[i].name == task_name:
                del tasks[i]
            else:
                i += 1

    @property
    def num_tasks(self) -> int:
        return len(self.tasks)

    def has_task(self, task_name: str) -> bool:
        for task in self.tasks:
            if task.name == task_name:
                return True
        return False

    def __contains__(self, task: 'Task') -> bool:
        return task in self.tasks

    def __lt__(self, other: 'Job') -> bool:
        # Needed for the operation of insort
        return self.run_at < other.run_at

    def __repr__(self) -> str:
        bundles_repr = ',\n        '.join(repr(task) for task in self.tasks)
        return (f'{self.__class__.__name__}(\n'
                f'    trigger_at = {self.run_at},\n'
                f'    handler_bundles = [\n'
                f'        {bundles_repr}\n'
                f'    ]\n'
                f')')
