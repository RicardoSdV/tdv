from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.user_options_entity import UserOption
from tdv.infra.database.tables import user_options_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class UserOptionsSerializer(BaseSerializer):
    _Entity: ClassVar[Type[UserOption]] = UserOption


class UserOptionsQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return user_options_table


class UserOptionsRepo(UserOptionsSerializer, UserOptionsQueryBuilder, BaseRepo):
    pass
