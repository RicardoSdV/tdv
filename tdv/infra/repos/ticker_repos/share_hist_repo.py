from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist
from tdv.infra.database.tables.ticker_tables import share_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class ShareHistSerializer(BaseSerializer):
    _Entity: ClassVar[Type[ShareHist]] = ShareHist


class ShareHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return share_hist_table


class ShareHistRepo(ShareHistSerializer, ShareHistQueryBuilder, BaseRepo):
    pass
