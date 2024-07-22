from typing import TYPE_CHECKING

from .do_once_job import DoOnceJob
from .repeat_always_job import RepeatAlwaysJob
from .repeat_until_job import RepeatUntilJob

types = ('DoOnceJob', 'RepeatAlwaysJob', 'RepeatUntilJob')

if TYPE_CHECKING:
    from typing import *

    Job  = Union[DoOnceJob, RepeatUntilJob, RepeatAlwaysJob]
    Jobs = Deque[Job]
    DoReSchedule = bool

    __all__ = types + ('Job', 'Jobs', 'DoReSchedule')
else:
    __all__ = types
