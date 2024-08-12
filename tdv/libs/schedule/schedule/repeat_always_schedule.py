from bisect import insort_right

from .. import Schedule


class RepeatAlwaysSchedule(Schedule):
    """ A Schedule specialised to hold only RepeatAlwaysJob(s)  """

    def run_pending(self) -> None:
        while self.jobs and self.jobs[0].run_at <= self.now():
            job = self.jobs.popleft()
            job()
            insort_right(self.jobs, job)
