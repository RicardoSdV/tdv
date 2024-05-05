from dataclasses import dataclass
from typing import Optional

from tdv.constants import Companies
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Company(Entity):
    id: Optional[int] = None
    abrv_name: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self):
        if self.abrv_name is not None:
            Companies.AbrvNames.validate_value(self.abrv_name)
        if self.name is not None:
            Companies.Names.validate_value(self.name)
