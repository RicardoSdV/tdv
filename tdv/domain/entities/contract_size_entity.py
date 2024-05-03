from typing import Optional

from tdv.domain.entities.base_entity import Entity, EntityEnum


class ContractSizes(EntityEnum):
    REGULAR = 100


class ContractSize(Entity):
    __slots__ = ('id', 'size', 'name')

    def __init__(
        self, contract_size_id: Optional[int] = None, size: Optional[int] = None, name: Optional[str] = None
    ) -> None:
        # TODO: Validate sizes and names
        self.id = contract_size_id
        self.size = size
        self.name = name
