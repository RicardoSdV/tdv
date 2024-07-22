from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.call_hist_entity import CallHist
from tdv.infra.database.tables.option_tables import call_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class CallHistSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[CallHist]]' = CallHist


class CallHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return call_hist_table


class CallHistRepo(CallHistSerializer, CallHistQueryBuilder, BaseRepo):
    pass
