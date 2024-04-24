from typing import Optional

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import ShareHistId, TickerId, InsertTimeId


class ShareHist(Entity):
    __slots__ = ('id', 'ticker_id', 'insert_time_id', 'price')

    def __init__(
            self,
            share_hist_id: Optional[ShareHistId] = None,
            ticker_id: Optional[TickerId] = None,
            insert_time_id: Optional[InsertTimeId] = None,
            price: Optional[float] = None
    ) -> None:
        self.id = share_hist_id
        self.ticker_id = ticker_id
        self.insert_time_id = insert_time_id
        self.price = price
