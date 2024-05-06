from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.constants import Exchanges, Currencies
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Exchange(Entity):

    id: Optional[int] = None
    abrv_name: Optional[str] = None
    name: Optional[str] = None
    currency: Optional[str] = None
    live: Optional[bool] = None
    hist: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.abrv_name is not None:
            Exchanges.AbrvNames.validate_value(self.abrv_name)
        if self.name is not None:
            Exchanges.Names.validate_value(self.name)
        if self.currency is not None:
            Currencies.validate_value(self.currency)
