from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import OptionChainId, TickerId


class OptionChain(Entity):
    __slots__ = ('id', 'ticker_id', 'underlying_price', 'expiry', 'is_call', 'created_at', 'updated_at')

    def __init__(self,
                 option_chain_id: Optional[OptionChainId] = None,
                 ticker_id: Optional[TickerId] = None,
                 underlying_price: Optional[float] = None,
                 is_call: Optional[bool] = None,
                 expiry: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 ) -> None:
        self.id = option_chain_id
        self.ticker_id = ticker_id
        self.underlying_price = underlying_price
        self.is_call = is_call
        self.expiry = expiry
        self.created_at = created_at
        self.updated_at = updated_at
