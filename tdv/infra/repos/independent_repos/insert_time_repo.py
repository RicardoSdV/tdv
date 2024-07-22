from typing import TYPE_CHECKING

from tdv.domain.entities.independent_entities.insert_time_entity import InsertTime
from tdv.infra.database.tables.independent_tables import insert_time_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class InsertTimeSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[InsertTime]]' = InsertTime


class InsertTimeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return insert_time_table


class InsertTimeRepo(InsertTimeSerializer, InsertTimeQueryBuilder, BaseRepo):
    pass
