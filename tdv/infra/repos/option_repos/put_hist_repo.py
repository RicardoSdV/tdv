from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.put_hist_entity import PutHist
from tdv.infra.database.tables.option_tables import put_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class PutHistSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[PutHist]]' = PutHist


class PutHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return put_hist_table


class PutHistRepo(PutHistSerializer, PutHistQueryBuilder, BaseRepo):
    pass
