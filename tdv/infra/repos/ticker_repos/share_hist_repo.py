from typing import TYPE_CHECKING

from tdv.domain.entities.ticker_entities.share_hist_entity import ShareHist
from tdv.infra.database.tables.ticker_tables import share_hist_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class ShareHistSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[ShareHist]]' = ShareHist


class ShareHistQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return share_hist_table


class ShareHistRepo(ShareHistSerializer, ShareHistQueryBuilder, BaseRepo):
    pass
