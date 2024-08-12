from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    from .. import Job, Task, Timestamp, TimeDelta


class RepeatAlwaysJob(Job):
    """ Holds one or more tasks. They are repeatedly called every interval from start.

    The operation is completely coupled to Schedule since it works by returning the next run_at time
    when called. After which the same instance is rescheduled to be run at the returned time. """

    __slots__ = ('interval', )

    def __init__(
            self,
            interval: 'TimeDelta',
            start   : 'Timestamp' = datetime.utcnow(),
            *tasks  : 'Task',
            name    :  str = '',
    ) -> None:
        super().__init__(start, name, *tasks)
        self.interval = interval

    def __call__(self) -> bool:
        for task in self.tasks:
            task()
        self.run_at += self.interval
        return True
