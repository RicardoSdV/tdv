from datetime import datetime
from typing import Optional

from tdv.domain.types import ExchangeId
from tdv.domain.entities.base_entity import Entity, EntityEnum


class Exchanges(EntityEnum):
    NEW_YORK = 'NYSE'


class Currencies(EntityEnum):
    US_DOLLAR = 'USD'


class Exchange(Entity):
    __slots__ = ('id', 'name', 'currency', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(self,
                 exchange_id: Optional[ExchangeId] = None,
                 name: Optional[str] = None,
                 currency: Optional[str] = None,
                 live: Optional[bool] = None,
                 hist: Optional[bool] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 ) -> None:
        super().__init__(entity_id=exchange_id)
        self.name: Optional[Exchanges] = None
        self.currency: Optional[Currencies] = None
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at

        if name is not None:
            self.set_name(name)

        if currency is not None:
            self.set_currency(currency)

    def set_name(self, name: str) -> None:
        Exchanges.assert_has_value(name)
        self.name = name

    def set_currency(self, currency: str) -> None:
        Currencies.assert_has_value(currency)
        self.currency = currency
