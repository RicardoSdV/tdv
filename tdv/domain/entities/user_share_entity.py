from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class UserShare(Entity):
    __slots__ = ('id', 'user_id', 'ticker_share_type_id', 'count', 'created_at', 'updated_at')

    def __init__(self,
                 user_share_id: Optional[int] = None,
                 user_id: Optional[int] = None,
                 ticker_share_type_id: Optional[int] = None,
                 count: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 ) -> None:
        self.id = user_share_id
        self.user_id = user_id
        self.ticker_share_type_id = ticker_share_type_id
        self.count = count
        self.created_at = created_at
        self.updated_at = updated_at
