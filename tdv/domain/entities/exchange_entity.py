from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


class Exchanges(EntityEnum):
    NEW_YORK = 'NYSE'
    LONDON = 'LSE'


class Currencies(EntityEnum):
    US_DOLLAR = 'USD'


class Exchange(Entity):
    __slots__ = ('id', 'name', 'currency', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        exchange_id: Optional[int] = None,
        name: Optional[str] = None,
        currency: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = exchange_id
        self.name = None if name is None else Exchanges.validate_value(name)
        self.currency = None if currency is None else Currencies.validate_value(currency)
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
