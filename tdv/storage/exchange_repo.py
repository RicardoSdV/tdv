from functools import cached_property
from typing import Dict

from sqlalchemy import Row, Table

from tdv.domain.entities.exchange import Exchange
from tdv.storage.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo
from tdv.storage.tables import exchanges_table


class ExchangeSerializer(BaseSerializer):
    def _to_instance(self, record: Row) -> Exchange:
        return Exchange(
            name=record[exchanges_table.c.name],
            exchange_id=record[exchanges_table.c.exchange_id],
            created_at=record[exchanges_table.c.created_at],
            updated_at=record[exchanges_table.c.updated_at],
        )

    def _to_dict(self, exchange: Exchange) -> Dict:
        return {'name': exchange.name}


class ExchangeQueryBuilder(BaseQueryBuilder):
    @cached_property
    def _table(self) -> Table:
        return exchanges_table


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    pass
