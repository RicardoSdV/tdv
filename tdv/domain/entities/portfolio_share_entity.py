from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity


class PortfolioShare(Entity):
    __slots__ = ('id', 'portfolio_id', 'ticker', 'ticker_share_type_id', 'count', 'created_at', 'updated_at')

    def __init__(self,
                 shares_id: Optional[int] = None,
                 portfolio_id: Optional[int] = None,
                 ticker: Optional[str] = None,
                 ticker_share_type_id: Optional[int] = None,
                 count: Optional[float] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 ) -> None:
        self.id = shares_id
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.ticker_share_type_id = ticker_share_type_id
        self.count = count
        self.created_at = created_at
        self.updated_at = updated_at
