from dataclasses import dataclass
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class ContractSize(Entity):
    # TODO: Validate sizes and names
    id: Optional[int] = None
    size: Optional[int] = None
    name: Optional[str] = None
