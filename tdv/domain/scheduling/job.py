from datetime import datetime
from typing import List

from tdv.domain.scheduling.task import Task


class Job:
    """A Job holds & calls one or more instances of Task, at a given time"""
    __slots__ = ('run_at', '__tasks')

    def __init__(self, run_at: datetime) -> None:
        self.run_at = run_at
        self.__tasks: List[Task] = []

    def __iadd__(self, task: Task) -> 'Job':
        self.__tasks.append(task)
        return self

    def __call__(self) -> None:
        for task in self.__tasks:
            task()

    def __lt__(self, time: datetime) -> bool:
        return self.run_at < time

    def __repr__(self) -> str:
        bundles_repr = ', '.join(repr(handler) for handler in self.__tasks)
        return f'TimeTriggeredEvent(trigger_at = {self.run_at}, handler_bundles = [{bundles_repr}]'
