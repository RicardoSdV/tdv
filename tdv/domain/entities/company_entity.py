from dataclasses import dataclass
from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


@dataclass
class Companies:
    class ShortNames(EntityEnum):
        TESLA = 'Tesla'

    class LongNames(EntityEnum):
        TESLA = 'Tesla Inc.'


class Company(Entity):
    __slots__ = ('id', 'long_name', 'short_name')

    def __init__(
        self,
        company_id: Optional[int] = None,
        long_name: Optional[str] = None,
        short_name: Optional[str] = None,
    ) -> None:
        self.id = company_id
        self.long_name = None if long_name is None else Companies.LongNames.validate_value(long_name)
        self.short_name = None if short_name is None else Companies.ShortNames.validate_value(short_name)