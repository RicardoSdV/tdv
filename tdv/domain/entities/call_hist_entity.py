from datetime import datetime
from typing import Optional

from pandas._libs.tslibs.timestamps import Timestamp

from tdv.domain.entities.base_entity import Entity, EntityEnum
from tdv.domain.types import OptionId, OptionChainId


class ContractSizes(EntityEnum):
    REGULAR = 100


class OptionHistory(Entity):
    __slots__ = (
        'id',
        'option_id',
        'last_trade_date',
        'last_price',
        'bid',
        'ask',
        'change',
        'volume',
        'open_interest',
        'implied_volatility',
        'size',
        'created_at',
    )

    def __init__(
        self,
        option_history_id: Optional[OptionId] = None,
        option_id: Optional[OptionChainId] = None,
        last_trade_date: Optional[Timestamp] = None,
        last_price: Optional[float] = None,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        change: Optional[float] = None,
        volume: Optional[int] = None,
        open_interest: Optional[int] = None,
        implied_volatility: Optional[float] = None,
        size: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = option_history_id
        self.option_id = option_id
        self.last_trade_date = last_trade_date
        self.last_price = last_price
        self.bid = bid
        self.ask = ask
        self.change = change
        self.volume = volume
        self.open_interest = open_interest
        self.implied_volatility = implied_volatility
        self.size = size
        self.created_at = created_at
