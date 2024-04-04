from datetime import datetime
from enum import Enum
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum
from tdv.domain.types import ExchangeId, TickerId


class TickersEnum(EntityEnum):
    TSLA = 'TSLA'
    AMZN = 'AMZN'


class Companies(EntityEnum):
    TSLA = 'Tesla'
    AMZN = 'Amazon'


class Ticker(Entity):
    __slots__ = ('id', 'exchange_id', 'ticker', 'company', 'live', 'hist', 'created_at', 'updated_at')

    def __init__(
        self,
        ticker_id: Optional[TickerId] = None,
        exchange_id: Optional[ExchangeId] = None,
        ticker_name: Optional[str] = None,
        company_name: Optional[str] = None,
        live: Optional[bool] = None,
        hist: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = ticker_id
        self.exchange_id = exchange_id
        self.ticker = None if ticker_name is None else TickersEnum.validate_value(ticker_name)
        self.company = None if company_name is None else Companies.validate_value(company_name)
        self.live = live
        self.hist = hist
        self.created_at = created_at
        self.updated_at = updated_at
