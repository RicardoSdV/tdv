from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class UserOption(Entity):
    __slots__ = ('id', 'user_id', 'option_id', 'count', 'created_at', 'updated_at')

    def __init__(self,
                 user_option_id: Optional[int] = None,
                 user_id: Optional[int] = None,
                 option_id: Optional[int] = None,
                 count: Optional[float] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 ) -> None:
        self.id = user_option_id
        self.user_id = user_id
        self.option_id = option_id
        self.count = count
        self.created_at = created_at
        self.updated_at = updated_at
