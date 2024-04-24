from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import StrikeId, ExpiryId


class Strike(Entity):
    __slots__ = ('id', 'expiry_id', 'strike_price')

    def __init__(
            self,
            strike_id: Optional[StrikeId] = None,
            expiry_id: Optional[ExpiryId] = None,
            strike_price: Optional[float] = None
    ) -> None:
        self.id = strike_id
        self.expiry_id = expiry_id
        self.strike_price = strike_price
