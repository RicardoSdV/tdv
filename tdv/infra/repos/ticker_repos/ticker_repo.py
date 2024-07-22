from typing import TYPE_CHECKING

from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
from tdv.infra.database.tables.ticker_tables import ticker_table
from tdv.infra.repos.base_repo import BaseRepo, BaseSerializer, BaseQueryBuilder

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class TickerSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[Ticker]]' = Ticker


class TickerQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return ticker_table


class TickerRepo(TickerSerializer, TickerQueryBuilder, BaseRepo):
    pass
