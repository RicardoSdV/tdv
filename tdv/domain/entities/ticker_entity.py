from datetime import datetime
from enum import Enum
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum
from tdv.domain.types import ExchangeId, TickerId


class Tickers(EntityEnum):
    TSLA = 'TSLA'
    AMZN = 'AMZN'


class Companies(Enum):
    TSLA = 'Tesla'
    AMZN = 'Amazon'


class Ticker(Entity):
    __slots__ = ('exchange_id', 'ticker', 'company', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        ticker_id: Optional[TickerId] = None,
        exchange_id: Optional[ExchangeId] = None,
        ticker: Optional[Tickers] = None,
        company: Optional[Companies] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(entity_id=ticker_id)
        self.exchange_id = exchange_id
        self.ticker = ticker
        self.company = company
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
