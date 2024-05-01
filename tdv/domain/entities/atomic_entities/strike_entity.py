from typing import Optional

from tdv.domain.entities.atomic_entities.base_entity import Entity


class Strike(Entity):
    __slots__ = ('id', 'expiry_id', 'strike_price')

    def __init__(
        self, strike_id: Optional[int] = None, expiry_id: Optional[int] = None, strike_price: Optional[float] = None
    ) -> None:
        self.id = strike_id
        self.expiry_id = expiry_id
        self.strike_price = strike_price
