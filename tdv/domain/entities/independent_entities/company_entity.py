from dataclasses import dataclass
from typing import Optional

from tdv.constants import Companies
from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True, repr=False)
class Company(Entity):
    id: Optional[int] = None
    long_name: Optional[str] = None
    short_name: Optional[str] = None

    def __post_init__(self) -> None:
        if self.long_name is not None:
            Companies.LongNames.validate_value(self.long_name)
        if self.short_name is not None:
            Companies.ShortNames.validate_value(self.short_name)
