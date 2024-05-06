from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class PortfolioOption(Entity):
    id: Optional[int] = None
    portfolio_id: Optional[int] = None
    strike_id: Optional[int] = None
    is_call: Optional[bool] = None
    count: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
