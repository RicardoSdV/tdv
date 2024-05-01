from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.option_hist_entity import OptionHist
from tdv.infra.database.tables import put_hist_table, call_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class OptionHistSerializer(BaseSerializer):
    _Entity: ClassVar[Type[OptionHist]] = OptionHist


class PutHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return put_hist_table


class CallHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return call_hist_table


class PutHistRepo(OptionHistSerializer, PutHistQueryBuilder, BaseRepo):
    pass


class CallHistRepo(OptionHistSerializer, CallHistQueryBuilder, BaseRepo):
    pass
