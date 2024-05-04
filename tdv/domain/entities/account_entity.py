from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


@dataclass(slots=True)
class Account(Entity):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
