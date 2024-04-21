from typing import Type, ClassVar

from sqlalchemy import Table

from tdv.domain.entities.portfolio_share_entity import PortfolioShare
from tdv.infra.database.tables import portfolio_share_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class PortfolioSharesSerializer(BaseSerializer):
    _Entity: ClassVar[Type[PortfolioShare]] = PortfolioShare


class PortfolioSharesQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_share_table


class PortfolioSharesRepo(PortfolioSharesSerializer, PortfolioSharesQueryBuilder, BaseRepo):
    pass
