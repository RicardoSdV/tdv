from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.contract_size_entity import ContractSize
from tdv.infra.database.tables import contract_size_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class ContractSizeSerializer(BaseSerializer):
    _Entity: ClassVar[Type[ContractSize]] = ContractSize


class ContractSizeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return contract_size_table


class ContractSizeRepo(ContractSizeSerializer, ContractSizeQueryBuilder, BaseRepo):
    pass
