from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class PortfolioShare(Entity):
    id: Optional[int] = None
    portfolio_id: Optional[int] = None
    ticker_id: Optional[int] = None
    count: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

