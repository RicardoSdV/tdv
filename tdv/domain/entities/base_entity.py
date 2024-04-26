from enum import Enum
from typing import Any, List, Dict, Tuple, TypeVar, Protocol

from tdv.domain.types import Insertable, KwArgs, Args


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
    """
    All entities should inherit from this, the base entity.

    One entity object represents a row of one of the tables of the database.

    Entities are responsible for data validation.

    Entities must have __slots__ with the exact same names as the column names they represent in DB tables.
    This is because the BaseRepo uses them to perform its default queries.
    """

    __slots__: Tuple[str, ...] = ()

    def __init__(self, *_: Args, **__: KwArgs) -> None:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.to_dict()})'

    def __eq__(self: T, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def to_dict(self) -> Dict[str, Insertable]:
        return {name: value for name in self.__slots__ if (value := getattr(self, name)) is not None}

    def to_list(self) -> List[Insertable]:
        return [attr for attr in (getattr(self, attr_name) for attr_name in self.__slots__) if attr is not None]

    def not_none_slots(self) -> List[str]:
        return [attr_name for attr_name in self.__slots__ if getattr(self, attr_name) is not None]
