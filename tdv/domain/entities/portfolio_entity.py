from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class Portfolio(Entity):
    __slots__ = ('id', 'account_id', 'name', 'cash', 'created_at', 'updated_at')

    def __init__(
        self,
        portfolio_id: Optional[int] = None,
        account_id: Optional[int] = None,
        name: Optional[str] = None,
        cash: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = portfolio_id
        self.account_id = account_id
        self.name = name
        self.cash = cash
        self.created_at = created_at
        self.updated_at = updated_at
