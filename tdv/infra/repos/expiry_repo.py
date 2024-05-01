from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.expiry_entity import Expiry
from tdv.infra.database.tables import expiry_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class ExpirySerializer(BaseSerializer):
    _Entity: ClassVar[Type[Expiry]] = Expiry


class ExpiryQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return expiry_table


class ExpiryRepo(ExpirySerializer, ExpiryQueryBuilder, BaseRepo):
    pass
