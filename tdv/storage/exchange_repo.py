from typing import Dict, List

from sqlalchemy import Row, Table, Connection, CursorResult, BinaryExpression

from tdv.constants import ExchangeNames
from tdv.domain.entities.exchange_entity import Exchange
from tdv.storage.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo
from tdv.storage.tables import exchanges_table


class ExchangeSerializer(BaseSerializer):
    def _to_instance(self, record: Row) -> Exchange:
        return Exchange(
            exchange_id=record[exchanges_table.c.exchange_id],
            name=record[exchanges_table.c.name],
            created_at=record[exchanges_table.c.created_at],
            updated_at=record[exchanges_table.c.updated_at],
        )

    def _to_dict(self, exchange: Exchange) -> Dict:
        return {'name': exchange.name}


class ExchangeQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchanges_table

    def _id_query(self) -> BinaryExpression:
        return self._table.c.id


class ExchangeRepo(ExchangeSerializer, ExchangeQueryBuilder, BaseRepo):
    def insert(self, conn: Connection, exchanges: List[Exchange]) -> CursorResult:
        return self._insert(conn, exchanges)

    def select(self, conn: Connection, exchanges: List[Exchange]) -> CursorResult:
        pass