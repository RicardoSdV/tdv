from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


class ContractSizes(EntityEnum):
    REGULAR = 100


class ContractSize(Entity):
    __slots__ = ('id', 'size')

    def __init__(
            self,
            contract_size_id: Optional[int] = None,
            size: Optional[int] = None
    ) -> None:
        self.id = contract_size_id
        self.size = size
