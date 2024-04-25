from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class PutHist(Entity):
    __slots__ = (
        'id',
        'strike_id',
        'insert_time_id',
        'last_trade_date',
        'last_price',
        'bid',
        'ask',
        'change',
        'volume',
        'open_interest',
        'implied_volatility',
    )

    def __init__(
        self,
        put_hist_id: Optional[int] = None,
        strike_id: Optional[int] = None,
        insert_time_id: Optional[int] = None,
        last_trade_date: Optional[datetime] = None,
        last_price: Optional[float] = None,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        change: Optional[float] = None,
        volume: Optional[int] = None,
        open_interest: Optional[int] = None,
        implied_volatility: Optional[float] = None,
    ) -> None:
        self.id = put_hist_id
        self.strike_id = strike_id
        self.insert_time_id = insert_time_id
        self.last_trade_date = last_trade_date
        self.last_price = last_price
        self.bid = bid
        self.ask = ask
        self.change = change
        self.volume = volume
        self.open_interest = open_interest
        self.implied_volatility = implied_volatility
