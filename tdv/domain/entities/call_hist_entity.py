from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class CallHist(Entity):
    id: Optional[int] = None
    strike_id: Optional[int] = None
    insert_time_id: Optional[int] = None
    last_trade_date: Optional[datetime] = None
    last_price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    change: Optional[float] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None
    implied_volatility: Optional[float] = None
