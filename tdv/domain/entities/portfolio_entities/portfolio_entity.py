from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class Portfolio(Entity):
    id: Optional[int] = None
    account_id: Optional[int] = None
    name: Optional[str] = None
    cash: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
