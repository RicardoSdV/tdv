from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import ContractSizeId


class ContractSize(Entity):
    __slots__ = ('id', 'size')

    def __init__(
            self,
            contract_size_id: Optional[ContractSizeId] = None,
            size: Optional[int] = None
    ) -> None:
        self.id = contract_size_id
        self.size = size
