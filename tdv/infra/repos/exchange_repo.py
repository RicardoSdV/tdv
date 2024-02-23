from functools import cached_property
from typing import Type

from sqlalchemy import Table, BinaryExpression

from tdv.domain.entities.exchange_entity import Exchange
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo
from tdv.infra.database.tables import exchanges_table


class ExchangeSerializer(BaseSerializer):
    @cached_property
    def _Entity(self) -> Type[Exchange]:
        return Exchange


class ExchangeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchanges_table

    def _id_query(self) -> BinaryExpression:
        return self._table.c.id


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    pass
