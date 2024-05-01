from typing import Type, ClassVar

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.ticker_entity import Ticker
from tdv.infra.database.tables import ticker_table
from tdv.infra.repos.base_repo import BaseRepo, BaseSerializer, BaseQueryBuilder


class TickerSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Ticker]] = Ticker


class TickerQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return ticker_table


class TickerRepo(TickerSerializer, TickerQueryBuilder, BaseRepo):
    pass
