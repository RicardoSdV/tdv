from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class InsertTime(Entity):
    id: Optional[int] = None
    time: Optional[datetime] = None
