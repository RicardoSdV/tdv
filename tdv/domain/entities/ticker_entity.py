from datetime import datetime
from typing import Optional

from tdv.constants import Tickers
from tdv.domain.entities.base_entity import Entity


class Ticker(Entity):
    __slots__ = ('id', 'exchange_id', 'company_id', 'name', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        ticker_id: Optional[int] = None,
        exchange_id: Optional[int] = None,
        company_id: Optional[int] = None,
        name: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = ticker_id
        self.exchange_id = exchange_id
        self.company_id = company_id
        self.name = None if name is None else Tickers.validate_value(name)
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
