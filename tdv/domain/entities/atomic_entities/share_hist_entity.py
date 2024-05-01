from typing import Optional

from tdv.domain.entities.atomic_entities.base_entity import Entity


class ShareHist(Entity):
    __slots__ = ('id', 'ticker_id', 'insert_time_id', 'price')

    def __init__(
        self,
        share_hist_id: Optional[int] = None,
        ticker_id: Optional[int] = None,
        insert_time_id: Optional[int] = None,
        price: Optional[float] = None,
    ) -> None:
        self.id = share_hist_id
        self.ticker_id = ticker_id
        self.insert_time_id = insert_time_id
        self.price = price
