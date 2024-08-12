from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from typing import *

    from .. import Job, Task, Timestamp, TimeDelta


class RepeatUntilJob(Job):
    """ Holds one or more tasks. They are repeatedly called every interval from start or now to finish.

    The operation is completely coupled to Schedule since it works by returning the next run_at time
    when called. After which the same instance is rescheduled to be run at the returned time, unless the
    returned time exceeds finish, then, returns None therefore job not rescheduled """

    __slots__ = ('interval', 'finish')

    def __init__(
            self,
            interval: 'TimeDelta',
            finish  : 'Timestamp',
            start   : 'Timestamp' = datetime.utcnow(),
            name    :  str = '',
            *tasks  : 'Task',
    ) -> None:
        super().__init__(start, name, *tasks)
        self.interval = interval
        self.finish   = finish

    def __call__(self) -> bool:
        for task in self.tasks:
            task()

        self.run_at += self.interval
        if self.run_at <= self.finish:
            return True
        return False
