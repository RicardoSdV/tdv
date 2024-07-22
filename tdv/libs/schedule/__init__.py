from typing import TYPE_CHECKING

from .schedule import Schedule
from .jobs import DoOnceJob, RepeatAlwaysJob, RepeatUntilJob
from .tasks import TaskNoArgs, TaskWithArgs

types = (
    'Schedule',
    'DoOnceJob', 'RepeatAlwaysJob', 'RepeatUntilJob',
    'TaskNoArgs', 'TaskWithArgs'
)

if TYPE_CHECKING:
    from .schedule import Offset, Threshold, NowStamper, JobName, JobNum
    from .jobs import Job, Jobs
    from .tasks import Task, Tasks, Handler

    __all__ = types + (
        'Offset', 'Threshold', 'NowStamper', 'JobName',
        'Job', 'Jobs',
        'Task', 'Tasks', 'Handler'
    )
