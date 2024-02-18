from typing import Dict, List

from sqlalchemy import Row, Table, Connection, CursorResult

from tdv.constants import ExchangeNames
from tdv.domain.entities.exchange_entity import Exchange
from tdv.storage.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo
from tdv.storage.tables import exchanges_table


class ExchangeSerializer(BaseSerializer):
    def _to_instance(self, record: Row) -> Exchange:
        return Exchange(
            name=ExchangeNames(record[exchanges_table.c.name]),
            exchange_id=record[exchanges_table.c.exchange_id],
            created_at=record[exchanges_table.c.created_at],
            updated_at=record[exchanges_table.c.updated_at],
        )

    def _to_dict(self, exchange: Exchange) -> Dict:
        return {'name': exchange.name.value}


class ExchangeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchanges_table


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    def insert(self, conn: Connection, exchange: Exchange) -> CursorResult:
        return self._insert(conn, exchange)

    def insert_many(self, conn: Connection, exchanges: List[Exchange]) -> CursorResult:
        return self._insert_many(conn, exchanges)
