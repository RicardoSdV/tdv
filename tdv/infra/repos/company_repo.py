from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.atomic_entities.company_entity import Company
from tdv.infra.database.tables import company_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class CompanySerializer(BaseSerializer):
    _Entity: ClassVar[Type[Company]] = Company


class CompanyQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return company_table


class CompanyRepo(CompanySerializer, CompanyQueryBuilder, BaseRepo):
    pass
