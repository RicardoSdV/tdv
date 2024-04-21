from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.option_chain_entity import OptionChain
from tdv.infra.database.tables import option_chain_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class OptionChainsSerializer(BaseSerializer):
    _Entity: ClassVar[Type[OptionChain]] = OptionChain


class OptionChainsQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return option_chain_table


class OptionChainsRepo(OptionChainsSerializer, OptionChainsQueryBuilder, BaseRepo):
    pass

