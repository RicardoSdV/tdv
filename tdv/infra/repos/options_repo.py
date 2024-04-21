from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.option_entity import Option
from tdv.infra.database.tables import option_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class OptionsSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Option]] = Option


class OptionsQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return option_table


class OptionsRepo(OptionsSerializer, OptionsQueryBuilder, BaseRepo):
    pass
