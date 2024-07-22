from typing import TYPE_CHECKING

from tdv.domain.entities.portfolio_entities.portfolio_share_entity import PortfolioShare
from tdv.infra.database.tables.portfolio_tables import portfolio_share_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class PortfolioShareSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[PortfolioShare]]' = PortfolioShare


class PortfolioShareQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return portfolio_share_table


class PortfolioShareRepo(PortfolioShareSerializer, PortfolioShareQueryBuilder, BaseRepo):
    pass
