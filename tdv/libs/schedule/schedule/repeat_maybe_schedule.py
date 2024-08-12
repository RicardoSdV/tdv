from bisect import insort_right

from .. import Schedule


class RepeatMaybeSchedule(Schedule):
    """ Can hold any type of job, will discard Job when ran, will reschedule RepeatAlwaysJob
    indefinitely, will reschedule RepeatUntilJob until finish. However, its less efficient,
    if only holding RepeatAlwaysJob use the RepeatAlwaysSchedule"""

    def run_pending(self) -> None:
        while self.jobs and self.jobs[0].run_at <= self.now():
            job = self.jobs.popleft()
            if job():
                insort_right(self.jobs, job)
