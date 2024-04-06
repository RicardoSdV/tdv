from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.exchange_entity import Exchange
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo
from tdv.infra.database.tables import exchanges_table


class ExchangeSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Exchange]] = Exchange


class ExchangeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchanges_table


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    pass
