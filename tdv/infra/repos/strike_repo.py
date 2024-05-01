from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.strike_entity import Strike
from tdv.infra.database.tables import strike_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class StrikeSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Strike]] = Strike


class StrikeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return strike_table


class StrikeRepo(StrikeSerializer, StrikeQueryBuilder, BaseRepo):
    pass
