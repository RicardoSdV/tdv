from typing import TYPE_CHECKING

from tdv.domain.entities.independent_entities.company_entity import Company
from tdv.infra.database.tables.independent_tables import company_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class CompanySerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[Company]]' = Company


class CompanyQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return company_table


class CompanyRepo(CompanySerializer, CompanyQueryBuilder, BaseRepo):
    pass
