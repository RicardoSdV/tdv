from datetime import datetime
from typing import Optional, Any

from tdv.constants import ExchangeNames
from tdv.domain.data_types import ExchangeId
from tdv.domain.entities.entity import Entity


class Exchange(Entity):
    __slots__ = ('id', 'name', 'created_at', 'updated_at')

    def __init__(
        self,
        exchange_id: Optional[ExchangeId] = None,
        name: Optional[ExchangeNames] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = exchange_id
        self.name = name.value
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, name={self.name}, created_at={self.created_at})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Exchange):
            return self.id == other.id and self.name == other.name
        return False
