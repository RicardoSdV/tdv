from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.constants import Tickers
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Ticker(Entity):
    id: Optional[int] = None
    exchange_id: Optional[int] = None
    company_id: Optional[int] = None
    name: Optional[str] = None
    live: Optional[bool] = None
    hist: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.name is not None:
            Tickers.validate_value(self.name)
