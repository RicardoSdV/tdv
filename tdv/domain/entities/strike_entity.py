from dataclasses import dataclass
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Strike(Entity):
    id: Optional[int] = None
    expiry_id: Optional[int] = None
    contract_size_id: Optional[int] = None
    strike_price: Optional[float] = None

