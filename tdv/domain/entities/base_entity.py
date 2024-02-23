from enum import Enum
from typing import Any, Optional, List

from tdv.domain.types import EntityId


class EntityEnum(Enum):
    """Simplify enum handling by inheriting from this class"""
    @classmethod
    def validate_value(cls, value: Any) -> Any:
        assert value in cls._value2member_map_
        return value

    @classmethod
    def to_list(cls) -> List[Any]:
        return [member.value for member in cls]


class Entity:
    """Base entity class, repo operation requires that __slots__ have the exact same name as table columns"""
    __slots__ = ('id',)

    def __init__(self, entity_id: Optional[EntityId]) -> None:
        self.id = entity_id

    def __repr__(self) -> str:
        slot_values = ', '.join(f'{name}={getattr(self, name)}' for name in self.__slots__)
        return f'{self.__class__.__name__}({slot_values})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False
