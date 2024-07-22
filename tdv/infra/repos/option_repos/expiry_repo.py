from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.expiry_entity import Expiry
from tdv.infra.database.tables.option_tables import expiry_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class ExpirySerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[Expiry]]' = Expiry


class ExpiryQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return expiry_table


class ExpiryRepo(ExpirySerializer, ExpiryQueryBuilder, BaseRepo):
    pass
