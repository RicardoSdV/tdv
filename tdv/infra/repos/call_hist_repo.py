from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.call_hist_entity import CallHist
from tdv.infra.database.tables import call_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class CallHistSerializer(BaseSerializer):
    _Entity: ClassVar[Type[CallHist]] = CallHist


class CallHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return call_hist_table


class CallHistRepo(CallHistSerializer, CallHistQueryBuilder, BaseRepo):
    pass
