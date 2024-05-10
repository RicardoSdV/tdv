from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.constants import EXCHANGE, CURRENCY
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class Exchange(Entity):

    id: Optional[int] = None
    name: Optional[str] = None
    long_name: Optional[str] = None
    currency: Optional[str] = None
    live: Optional[bool] = None
    hist: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.name is not None:
            EXCHANGE.NAME.validate_value(self.name)
        if self.long_name is not None:
            EXCHANGE.LONG_NAME.validate_value(self.long_name)
        if self.currency is not None:
            CURRENCY.validate_value(self.currency)
