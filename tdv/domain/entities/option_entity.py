from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import OptionId, OptionChainId


class Option(Entity):
    __slots__ = ('id', 'option_chain_id', 'strike', 'last_trade', 'last_price', 'bid', 'ask', 'change',
                 'volume', 'open_interest', 'implied_volatility', 'created_at', 'updated_at')

    def __init__(
            self,
            option_id: Optional[OptionId] = None,
            option_chain_id: Optional[OptionChainId] = None,
            strike: Optional[float] = None,
            last_trade: Optional[float] = None,
            last_price: Optional[float] = None,
            bid: Optional[float] = None,
            ask: Optional[float] = None,
            change: Optional[float] = None,
            volume: Optional[int] = None,
            open_interest: Optional[int] = None,
            implied_volatility: Optional[float] = None,
            created_at: Optional[datetime] = None,
    ) -> None:
        self.id = option_id
        self.option_chain_id = option_chain_id
        self.strike = strike
        self.last_trade = last_trade
        self.last_price = last_price
        self.bid = bid
        self.ask = ask
        self.change = change
        self.volume = volume
        self.open_interest = open_interest
        self.implied_volatility = implied_volatility
        self.created_at = created_at
