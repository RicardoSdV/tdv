from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Expiry(Entity):
    id: Optional[int] = None
    ticker_id: Optional[int] = None
    date: Optional[datetime] = None

