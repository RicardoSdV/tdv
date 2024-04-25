from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.put_hist_entity import PutHist
from tdv.infra.database.tables import put_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PutHistSerializer(BaseSerializer):
    _Entity: ClassVar[Type[PutHist]] = PutHist


class PutHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return put_hist_table


class PutHistRepo(PutHistSerializer, PutHistQueryBuilder, BaseRepo):
    pass
