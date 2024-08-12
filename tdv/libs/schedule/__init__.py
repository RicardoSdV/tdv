from typing import TYPE_CHECKING

from .tasks.task import Task
from .tasks.task_with_args import TaskWithArgs

from .jobs.job import Job
from .jobs.repeat_always_job import RepeatAlwaysJob
from .jobs.repeat_until_job import RepeatUntilJob

from .schedule.schedule import Schedule

types = (
    'Task', 'TaskWithArgs',
    'Job', 'RepeatAlwaysJob', 'RepeatUntilJob',
    'Schedule',
)

if TYPE_CHECKING:
    from datetime import datetime, timedelta

    # As long as all the jobs in the schedule & schedule itself use the same date format, any date format is
    # valid, given that they can be compared. By default, it works with datetime objects & timedeltas, so
    # whatever other stamp used should mimic their operation, for example, you can pass unix stamps as dates
    # & add or subtract more unix stamps as deltas and so on. Or use pandas or numpy stamps or whatever.
    Timestamp = datetime
    TimeDelta = timedelta

    __all__ = types + ('Timestamp', 'TimeDelta')

else:
    __all__ = types

