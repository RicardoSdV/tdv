from dataclasses import dataclass
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class ShareHist(Entity):
    id: Optional[int] = None
    ticker_id: Optional[int] = None
    insert_time_id: Optional[int] = None
    price: Optional[float] = None
