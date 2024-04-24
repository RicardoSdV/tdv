from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import CompanyId


class Company(Entity):
    __slots__ = ('id', 'name', 'short_name')

    def __init__(
            self,
            company_id: Optional[CompanyId] = None,
            name: Optional[str] = None,
            short_name: Optional[str] = None
    ) -> None:
        self.id = company_id
        self.name = name
        self.short_name = short_name
