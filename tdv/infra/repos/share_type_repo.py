from sqlalchemy import Table

from tdv.domain.entities.ticker_share_type_entity import TickerShareType
from tdv.infra.database.tables import ticker_share_type_table
from tdv.infra.repos.base_repo import BaseRepo, BaseSerializer, BaseQueryBuilder


class ShareTypeSerializer(BaseSerializer):
    _Entity = TickerShareType


class ShareTypeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return ticker_share_type_table


class ShareTypeRepo(BaseRepo, ShareTypeSerializer, ShareTypeQueryBuilder):
    pass
