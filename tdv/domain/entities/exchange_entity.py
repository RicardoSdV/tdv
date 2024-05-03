from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


class ExchangeAbrvs(EntityEnum):
    NEW_YORK = 'NYSE'


class ExchangeNames(EntityEnum):
    NEW_YORK = 'New York Stock Exchange'


class Currencies(EntityEnum):
    US_DOLLAR = 'USD'


class Exchange(Entity):
    __slots__ = ('id', 'name', 'abrv_name', 'currency', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        exchange_id: Optional[int] = None,
        name: Optional[str] = None,
        abrv_name: Optional[str] = None,
        currency: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = exchange_id
        self.name = None if name is None else ExchangeNames.validate_value(name)
        self.abrv_name = None if abrv_name is None else ExchangeAbrvs.validate_value(abrv_name)
        self.currency = None if currency is None else Currencies.validate_value(currency)
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
