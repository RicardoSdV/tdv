from bisect import insort_right
from collections import deque
from datetime import datetime
from typing import TYPE_CHECKING

from schedule import Scheduler

Scheduler()

if TYPE_CHECKING:
    from typing import *
    from datetime import timedelta

    from tdv.libs.schedule.jobs import Job, Jobs
    from tdv.libs.schedule.tasks import Task

    Offset     = Optional[timedelta]  # To run jobs before their time to compensate for run time, or other reasons
    Threshold  = Optional[timedelta]  # To delete old jobs that couldn't be run bc jobs piling up or other reasons
    NowStamper = Callable[[], datetime]  # NowStamper provides the reference of what is now_stamp_maker
    JobName    = str
    JobNum     = int

class RepeatAlwaysSchedule:
    """
    Holds a list of Job, can be run based on their run_at attr, optionally applying a __run_at_offset.
    Can discard events that are further in the past than the __delete_threshold.

    RepeatAlwaysSchedule is specifically designed to hold RepeatAlwaysJob(s) more efficiently, since
    it does not need to check weather or not the job needs to be rescheduled, however, it does not

    """

    __slots__ = ('jobs', 'run_at_offset', 'delete_threshold', 'now_stamp_maker')

    def __init__(
            self,
            run_at_offset   : 'Offset'     = None,
            delete_threshold: 'Threshold'  = None,
            now_stamp_maker : 'NowStamper' = datetime.utcnow,
    ) -> None:
        # The deque of jobs is sorted on insert in chronological order based on their run_at. Jobs are popped left to
        # be run, at best appended to be added to the deque. But could need to be inserted in O(n) were n is the number
        # of jobs that are further in the future than the one being inserted.
        self.jobs: 'Jobs' = deque()  # DANGER: The execution order of the jobs depends on insort_right to add jobs

        self.run_at_offset    = run_at_offset
        self.delete_threshold = delete_threshold

        # Dependencies
        self.now_stamp_maker = now_stamp_maker

    def __iadd__(self, job: 'Job') -> 'Schedule':
        insort_right(self.jobs, job)
        return self

    def __isub__(self, job: 'Job') -> 'Schedule':
        self.jobs.remove(job)
        return self

    def __contains__(self, name: 'JobName') -> bool:
        for job in self.jobs:
            if job.name == name:
                return True
        return False

    def __len__(self) -> 'JobNum':
        return len(self.jobs)

    def run_pending(self) -> None:
        while self.jobs and self.jobs[0].run_at <= self.__offset_now:
            job = self.jobs.popleft()
            print(repr(job))
            if job():
                insort_right(self.jobs, job)

    @property
    def __offset_now(self) -> 'datetime':
        if self.run_at_offset is None:
            return self.now_stamp_maker()
        return self.now_stamp_maker() + self.run_at_offset

    def del_old_jobs(self) -> None:
        while self.jobs and self.jobs[-1].run_at < self.__delete_time:
            self.jobs.pop()

    @property
    def __delete_time(self) -> 'datetime':
        if self.delete_threshold is None:
            return self.now_stamp_maker()
        return self.now_stamp_maker() - self.delete_threshold

    def remove_jobs_by_name(self, name: 'JobName') -> None:
        for job in self.jobs:
            if job.name == name:
                self.jobs.remove(job)

    def add_task_to_job(self, name: 'JobName', task: 'Task') -> None:
        """ If two jobs have the same name the task will be added to both """
        for job in self.jobs:
            if job.name == name:
                job.tasks.append(task)

    # No found use ATM
    # @property
    # def next_job_time(self) -> 'Optional[datetime]':
    #     if self.jobs:
    #         return self.jobs[0].run_at
    #     return None
