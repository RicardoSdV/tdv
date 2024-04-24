from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import ExpiryId, ContractSizeId, TickerId


class Expiry(Entity):
    __slots__ = ('id', 'ticker_id', 'contract_size_id', 'expiry_date')

    def __init__(
            self,
            expiry_id: Optional[ExpiryId] = None,
            ticker_id: Optional[TickerId] = None,
            contract_size_id: Optional[ContractSizeId] = None,
            expiry_date: Optional[datetime] = None
    ) -> None:
        self.id = expiry_id
        self.ticker_id = ticker_id
        self.contract_size_id = contract_size_id
        self.expiry_date = expiry_date
