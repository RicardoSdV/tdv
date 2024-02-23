from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import OptionId


class Option(Entity):
    __slots__ = ('strike', 'last_trade', 'last_price', 'bid', 'ask', 'change', 'volume',
                 'interest', 'volatility', 'in_money', 'created_at', 'updated_at')

    def __init__(
            self,
            option_id: Optional[OptionId],
            strike: Optional[float],
            last_trade: Optional[float],
            last_price: Optional[float],
            bid: Optional[float],
            ask: Optional[float],
            change: Optional[float],
            volume: Optional[int],
            interest: Optional[int],
            volatility: Optional[float],
            in_money: Optional[int],
            created_at: Optional[datetime],
            updated_at: Optional[datetime],
    ) -> None:
        super().__init__(option_id)
        self.strike = strike
        self.last_trade = last_trade
        self.last_price = last_price
        self.bid = bid
        self.ask = ask
        self.change = change
        self.volume = volume
        self.interest = interest
        self.volatility = volatility
        self.in_money = in_money
        self.created_at = created_at
        self.updated_at = updated_at
