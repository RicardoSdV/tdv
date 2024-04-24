from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import PortfolioShareId, PortfolioId, TickerId


class PortfolioShare(Entity):
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
        share_id: Optional[PortfolioShareId] = None,
        portfolio_id: Optional[PortfolioId] = None,
        ticker_id: Optional[TickerId] = None,
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
