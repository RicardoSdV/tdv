from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.portfolio_entity import Portfolios
from tdv.infra.database.tables import portfolio_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfoliosSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Portfolios]] = Portfolios


class PortfoliosQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_table


class PortfoliosRepo(PortfoliosSerializer, PortfoliosQueryBuilder, BaseRepo):
    pass
