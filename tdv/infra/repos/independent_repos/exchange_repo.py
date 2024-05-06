from typing import ClassVar, Type, List

from sqlalchemy import Table, Connection

from tdv.domain.entities.independent_entities.exchange_entity import Exchange
from tdv.infra.database.tables.independent_tables import exchange_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo, EntityT


class ExchangeSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Exchange]] = Exchange


class ExchangeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchange_table


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    pass
