from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.strike_entity import Strike
from tdv.infra.database.tables.option_tables import strike_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class StrikeSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[Strike]]' = Strike


class StrikeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return strike_table


class StrikeRepo(StrikeSerializer, StrikeQueryBuilder, BaseRepo):
    pass
