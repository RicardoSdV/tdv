from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class Portfolio(Entity):
    __slots__ = (
        'id',
        'user_id',
        'portfolio_shares_id',
        'portfolio_options_id',
        'cash',
        'created_at',
        'updated_at',
    )

    def __init__(
        self,
        portfolio_id: Optional[int] = None,
        user_id: Optional[int] = None,
        portfolio_shares_id: Optional[int] = None,
        portfolio_options_id: Optional[int] = None,
        cash: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = portfolio_id
        self.user_id = user_id
        self.portfolio_shares_id = portfolio_shares_id
        self.portfolio_options_id = portfolio_options_id
        self.cash = cash
        self.created_at = created_at
        self.updated_at = updated_at
