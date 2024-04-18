from typing import Type, ClassVar

from sqlalchemy import Table

from tdv.domain.entities.user_share_entity import UserShare
from tdv.infra.database.tables import portfolio_shares_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class UserSharesSerializer(BaseSerializer):
    _Entity: ClassVar[Type[UserShare]] = UserShare


class UserSharesQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return portfolio_shares_table


class UserSharesRepo(UserSharesSerializer, UserSharesQueryBuilder, BaseRepo):
    pass
