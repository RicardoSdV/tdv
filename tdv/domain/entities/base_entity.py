from enum import Enum
from typing import Any, Optional, List, Dict, Tuple, TypeVar, Generic, Protocol

from tdv.domain.types import EntityId, AttrName, Insertable, KwArgs, Args


class EntityEnum(Enum):
    """Simplify enum handling by inheriting from this class"""

    @classmethod
    def validate_value(cls, value: Any) -> Any:
        assert value in cls._value2member_map_
        return value

    @classmethod
    def to_list(cls) -> List[Any]:
        return [member.value for member in cls]


T = TypeVar('T', bound='EntityProtocol')


class EntityProtocol(Protocol):
    id: Any


class Entity:
    """Base entity class, repo operation requires that __slots__ have the exact same name as table columns"""

    __slots__: Tuple[str, ...] = ()

    def __init__(self, *_: Args, **__: KwArgs) -> None:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.to_dict()})'

    def __eq__(self: T, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def to_dict(self) -> Dict[AttrName, Insertable]:
        return {name: value for name in self.__slots__ if (value := getattr(self, name)) is not None}

    def to_list(self) -> List[Insertable]:
        return [attr for attr in (getattr(self, attr_name) for attr_name in self.__slots__) if attr is not None]

    def not_none_slots(self) -> List[AttrName]:
        return [attr_name for attr_name in self.__slots__ if getattr(self, attr_name) is not None]
