from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class Expiry(Entity):
    __slots__ = ('id', 'ticker_id', 'date')

    def __init__(
        self,
        expiry_id: Optional[int] = None,
        ticker_id: Optional[int] = None,
        date: Optional[datetime] = None,
    ) -> None:
        self.id = expiry_id
        self.ticker_id = ticker_id
        self.date = date
