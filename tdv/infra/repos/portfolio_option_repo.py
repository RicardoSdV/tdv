from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.portfolio_option_entity import PortfolioOption
from tdv.infra.database.tables import portfolio_option_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioOptionSerializer(BaseSerializer):
    _Entity: ClassVar[Type[PortfolioOption]] = PortfolioOption


class PortfolioOptionQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_option_table


class PortfolioOptionRepo(PortfolioOptionSerializer, PortfolioOptionQueryBuilder, BaseRepo):
    pass
