from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.exchange_entity import Exchange
from tdv.infra.database.tables import option_chains_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class OptionChainsSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Exchange]] = Exchange


class OptionChainsQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return option_chains_table


class OptionChainsRepo(OptionChainsSerializer, OptionChainsQueryBuilder, BaseRepo):
    pass

