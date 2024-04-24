from datetime import datetime
from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import PortfolioId, AccountId


class Portfolio(Entity):
    __slots__ = (
        'id',
        'account_id',
        'cash',
        'created_at',
        'updated_at',
    )

    def __init__(
        self,
        portfolio_id: Optional[PortfolioId] = None,
        account_id: Optional[AccountId] = None,
        cash: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = portfolio_id
        self.account_id = account_id
        self.cash = cash
        self.created_at = created_at
        self.updated_at = updated_at
