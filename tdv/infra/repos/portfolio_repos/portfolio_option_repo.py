from typing import TYPE_CHECKING

from tdv.domain.entities.portfolio_entities.portfolio_option_entity import PortfolioOption
from tdv.infra.database.tables.portfolio_tables import portfolio_option_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class PortfolioOptionSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[PortfolioOption]]' = PortfolioOption


class PortfolioOptionQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return portfolio_option_table


class PortfolioOptionRepo(PortfolioOptionSerializer, PortfolioOptionQueryBuilder, BaseRepo):
    pass
