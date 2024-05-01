from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class InsertTime(Entity):
    __slots__ = ('id', 'time')

    def __init__(self, insert_time_id: Optional[int] = None, time: Optional[datetime] = None) -> None:
        self.id = insert_time_id
        self.time = time
