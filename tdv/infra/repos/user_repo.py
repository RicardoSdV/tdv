from functools import cached_property
from typing import Type

from sqlalchemy import Table

from tdv.domain.entities.user_entity import User
from tdv.infra.database.tables import users_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class UserSerializer(BaseSerializer):
    _Entity = User


class UserQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return users_table


class UserRepo(UserSerializer, UserQueryBuilder, BaseRepo):
    pass
