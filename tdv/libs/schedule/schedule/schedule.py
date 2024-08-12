from bisect import insort_right
from collections import deque
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    from .. import Job, Task, Timestamp


class Schedule:
    __slots__ = ('jobs', 'now', 'rem_job')

    def __init__(
            self,
            *jobs: 'Job',
            now: Callable = datetime.utcnow,
    ) -> None:
        # The deque of jobs is sorted on insert in chronological order based on their run_at. Jobs are popped left to
        # be run, at best appended to be added to the deque. But could need to be inserted in O(n) were n is the number
        # of jobs that are further in the future than the one being inserted. (Not totally true but good enough)
        self.jobs: 'Deque[Job]' = deque()  # DANGER: The execution order of the jobs depends on insort_right to add jobs
        self.add_jobs(*jobs)
        self.now = now
        self.rem_job = self.jobs.remove

    def add_job(self, job: 'Job') -> None:
        insort_right(self.jobs, job)

    def add_jobs(self, *jobs: 'Job') -> None:
        for job in jobs:
            insort_right(self.jobs, job)

    def del_old_jobs(self, now: 'Timestamp' = datetime.utcnow()) -> None:
        jobs, pop_job = self.jobs, self.jobs.popleft
        while jobs and jobs[-1].run_at < now:
            pop_job()

    def run_pending(self) -> None:
        # No locals declared because num calls to run_pending expected > num jobs run
        while self.jobs and self.jobs[0].run_at <= self.now():
            self.jobs.popleft()()

    def rem_job_by_name(self, job_name: str) -> None:
        for i, job in enumerate(self.jobs):
            if job.name == job_name:
                del self.jobs[i]
                return

    def rem_jobs_by_name(self, job_name: str):
        i, jobs, len_jobs = 0, self.jobs, len(self.jobs)
        while i < len_jobs:
            if jobs[i].name == job_name:
                del jobs[i]
                len_jobs -= 1
            else:
                i += 1

    def add_task_to_job(self, job_name: str, task: 'Task') -> None:
        """ If two jobs have the same name the task will be added to both """
        for job in self.jobs:
            if job.name == job_name:
                job.add_task(task)
