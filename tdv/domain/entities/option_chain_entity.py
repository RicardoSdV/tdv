from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import OptionChainId, TickerId





class OptionChain(Entity):
    __slots__ = ('ticker_id', 'ticker', 'expiry', 'is_call', 'size', 'currency', 'created_at', 'updated_at')

    def __init__(self,
                 option_chain_id: Optional[OptionChainId],
                 ticker_id: Optional[TickerId],
                 expiry: Optional[datetime],
                 is_call: Optional[bool],
                 size: Optional[int],
                 created_at: Optional[datetime],
                 updated_at: Optional[datetime],
                 ) -> None:
        super().__init__(option_chain_id)
        self.ticker_id = ticker_id
        self.expiry = expiry
        self.is_call = is_call
        self.size = size
        self.created_at = created_at
        self.updated_at = updated_at
