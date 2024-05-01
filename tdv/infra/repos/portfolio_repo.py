from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.portfolio_entity import Portfolio
from tdv.infra.database.tables import portfolio_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Portfolio]] = Portfolio


class PortfolioQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_table


class PortfolioRepo(PortfolioSerializer, PortfolioQueryBuilder, BaseRepo):
    pass
