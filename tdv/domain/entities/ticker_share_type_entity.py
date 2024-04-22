from typing import Optional

from tdv.domain.entities.base_entity import EntityEnum, Entity


class ShareTypes(EntityEnum):
    ORDINARY = 'ordinary'
    PREFERENCE = 'preference'


class TickerShareType(Entity):
    __slots__ = ('id', 'ticker_id', 'share_type')

    def __init__(
        self,
        ticker_share_type_id: Optional[int] = None,
        ticker_id: Optional[int] = None,
        share_type: Optional[str] = None,
    ) -> None:
        self.id = ticker_share_type_id
        self.ticker_id = ticker_id
        self.share_type = None if share_type is None else ShareTypes.validate_value(share_type)
