from dataclasses import dataclass
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class Strike(Entity):
    id: Optional[int] = None
    expiry_id: Optional[int] = None
    contract_size_id: Optional[int] = None
    price: Optional[float] = None
