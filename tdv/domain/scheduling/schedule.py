from bisect import insort_right
from collections import deque
from datetime import timedelta, datetime
from typing import Optional, Deque

from tdv.domain.scheduling.job import Job


class Schedule:
    """
    Holds a list of jobs, which can be run based on their run_at attr, optionally applying an offset.
    Can discard events that are further in the past than the threshold.
    """

    __slots__ = ('__jobs', '__run_offset', '__delete_offset')

    def __init__(self, offset: Optional[timedelta] = None, threshold: Optional[timedelta] = None) -> None:
        # The deque of jobs is sorted on insert in chronological order based on their run_at. Jobs are popped left to
        # be run, and, best case scenario appended to be added to the deque. But could need to be inserted in O(n)
        # were n is the number of jobs that are further in the future than the one being inserted.
        self.__jobs: Deque[Job] = deque()
        self.__run_offset = offset
        self.__delete_offset = threshold

    def __iadd__(self, job: Job) -> 'Schedule':
        insort_right(self.__jobs, job)
        return self

    @property
    def next_job_time(self) -> Optional[datetime]:
        if self.__jobs:
            return self.__jobs[0].run_at
        return None

    def run_pending(self) -> None:
        run_time = self.__run_time()
        while self.__jobs and self.__jobs[0].run_at <= run_time:
            job = self.__jobs.popleft()
            job()

    def delete_old_jobs(self) -> None:
        delete_time = self.__delete_time()
        while self.__jobs and self.__jobs[-1].run_at < delete_time:
            self.__jobs.pop()

    def __run_time(self) -> datetime:
        if self.__run_offset is None:
            return datetime.utcnow()
        return datetime.utcnow() + self.__run_offset

    def __delete_time(self) -> datetime:
        if self.__delete_offset is None:
            return datetime.utcnow() - timedelta(days=1)
        else:
            return datetime.utcnow() - self.__delete_offset
