from functools import cached_property
from typing import Type

from sqlalchemy import Table

from tdv.domain.entities.ticker_share_type_entity import TickerShareType
from tdv.infra.database.tables import ticker_share_types_table
from tdv.infra.repos.base_repo import BaseRepo, BaseSerializer, BaseQueryBuilder


class ShareTypeSerializer(BaseSerializer):
    @cached_property
    def _Entity(self) -> Type[TickerShareType]:
        return TickerShareType


class ShareTypeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return ticker_share_types_table


class ShareTypeRepo(BaseRepo, ShareTypeSerializer, ShareTypeQueryBuilder):
    pass