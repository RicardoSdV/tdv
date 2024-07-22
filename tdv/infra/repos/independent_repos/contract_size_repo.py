from typing import TYPE_CHECKING

from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
from tdv.infra.database.tables.independent_tables import contract_size_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class ContractSizeSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[ContractSize]]' = ContractSize


class ContractSizeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return contract_size_table


class ContractSizeRepo(ContractSizeSerializer, ContractSizeQueryBuilder, BaseRepo):
    pass
