from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.portfolio_option_entity import PortfolioOption
from tdv.infra.database.tables import portfolio_options_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioOptionsSerializer(BaseSerializer):
    _Entity: ClassVar[Type[PortfolioOption]] = PortfolioOption


class PortfolioOptionsQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_options_table


class PortfolioOptionsRepo(PortfolioOptionsSerializer, PortfolioOptionsQueryBuilder, BaseRepo):
    pass
