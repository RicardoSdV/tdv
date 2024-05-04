from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.constants import Exchanges, Currencies
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Exchange(Entity):

    id: Optional[int] = None
    name: Optional[str] = None
    long_name: Optional[str] = None
    currency: Optional[str] = None
    live: Optional[bool] = None
    hist: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.name is not None:
            Exchanges.ShortNames.validate_value(self.name)
        if self.long_name is not None:
            Exchanges.LongNames.validate_value(self.long_name)
        if self.currency is not None:
            Currencies.validate_value(self.currency)

