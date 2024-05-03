from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class PortfolioOption(Entity):
    __slots__ = ('id', 'portfolio_id', 'strike_id', 'is_call', 'count', 'created_at', 'updated_at')

    def __init__(
        self,
        user_option_id: Optional[int] = None,
        portfolio_id: Optional[int] = None,
        strike_id: Optional[int] = None,
        is_call: Optional[bool] = None,
        count: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = user_option_id
        self.portfolio_id = portfolio_id
        self.strike_id = strike_id
        self.is_call = is_call
        self.count = count
        self.created_at = created_at
        self.updated_at = updated_at
