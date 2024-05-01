from typing import Type, ClassVar

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.portfolio_share_entity import PortfolioShare
from tdv.infra.database.tables import portfolio_share_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioShareSerializer(BaseSerializer):
    _Entity: ClassVar[Type[PortfolioShare]] = PortfolioShare


class PortfolioShareQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_share_table


class PortfolioShareRepo(PortfolioShareSerializer, PortfolioShareQueryBuilder, BaseRepo):
    pass
