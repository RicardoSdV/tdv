from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio
from tdv.infra.database.tables.portfolio_tables import portfolio_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Portfolio]] = Portfolio


class PortfolioQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_table


class PortfolioRepo(PortfolioSerializer, PortfolioQueryBuilder, BaseRepo):
    pass
