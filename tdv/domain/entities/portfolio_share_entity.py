from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class PfolShare(Entity):
    __slots__ = (
        'id',
        'portfolio_id',
        'ticker_id',
        'count',
        'created_at',
        'updated_at',
    )

    def __init__(
        self,
        share_id: Optional[int] = None,
        portfolio_id: Optional[int] = None,
        ticker_id: Optional[int] = None,
        count: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = share_id
        self.portfolio_id = portfolio_id
        self.ticker_id = ticker_id
        self.count = count
        self.created_at = created_at
        self.updated_at = updated_at
