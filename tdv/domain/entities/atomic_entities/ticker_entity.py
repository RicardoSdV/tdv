from datetime import datetime
from typing import Optional

from tdv.domain.entities.atomic_entities.base_entity import Entity, EntityEnum


class Tickers(EntityEnum):
    TSLA = 'TSLA'


class Ticker(Entity):
    __slots__ = ('id', 'exchange_id', 'company_id', 'ticker_name', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        ticker_id: Optional[int] = None,
        exchange_id: Optional[int] = None,
        company_id: Optional[int] = None,
        ticker_name: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = ticker_id
        self.exchange_id = exchange_id
        self.company_id = company_id
        self.ticker_name = None if ticker_name is None else Tickers.validate_value(ticker_name)
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
