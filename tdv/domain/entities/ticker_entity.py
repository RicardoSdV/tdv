from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


class Tickers(EntityEnum):
    TSLA = 'TSLA'


class Companies(EntityEnum):
    TSLA = 'Tesla'


class Ticker(Entity):
    __slots__ = ('id', 'exchange_id', 'ticker', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        ticker_id: Optional[int] = None,
        exchange_id: Optional[int] = None,
        ticker_name: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = ticker_id
        self.ticker = None if ticker_name is None else Tickers.validate_value(ticker_name)
        self.exchange_id = exchange_id
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
