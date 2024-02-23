from collections import defaultdict
from functools import cached_property
from typing import Dict, Iterable, Tuple, List, Type

from sqlalchemy import CursorResult, Insert, Table, Connection, Select, ColumnElement, Column, and_, bindparam, Row

from tdv.domain.entities.base_entity import Entity


class BaseSerializer:
    @cached_property
    def _Entity(self) -> Type[Entity]:
        """Must override with the domain/entities entity that belongs to the overriding subclass"""
        raise NotImplementedError()

    def _to_entities(self, result: CursorResult) -> List[Entity]:
        """Turn Row objects into domain/entities with Nones for missing columns"""
        return [self._Entity(**self._row_to_dict(row)) for row in result]

    def _entity_to_dict(self, entities: Iterable[Entity]) -> Dict:
        """Turns domain/entities into param dicts of not None params"""
        params = defaultdict(list)
        for entity in entities:
            for attr_name in self._Entity.__slots__:
                attr = getattr(entity, attr_name)
                if attr is not None:
                    params[f'b_{attr_name}'].append(attr)
        return params

    @staticmethod
    def _row_to_dict(row: Row) -> Dict:
        return {n: getattr(row, n) for n in row.keys()}


class BaseQueryBuilder:
    @cached_property
    def _table(self) -> Table:
        """Must override with the table from database/tables that belongs to the overriding subclass"""
        raise NotImplementedError()

    @cached_property
    def _primary_key_columns(self) -> Tuple[Column, ...]:
        return tuple(c for c in self._table.c if c.primary_key)  # Pycharm thinks _table.c isn't iterable, it's wrong.

    @cached_property
    def _primary_keys_query(self) -> ColumnElement:
        return and_(*(c == bindparam(f'b_{c.name}') for c in self._primary_key_columns))

    def _insert_query(self) -> Insert:
        return self._table.insert()

    def _select_query(self) -> Select:
        return self._table.select()

    def _get_by_id_query(self) -> Select:
        return self._select_query().where(self._primary_keys_query)

    @staticmethod
    def _make_for_update(query: Select, key_share: bool = True) -> Select:
        return query.with_for_update(key_share=key_share)


class BaseRepo(BaseQueryBuilder, BaseSerializer):
    def _insert(self, conn: Connection, instances: Iterable[Entity]) -> List[Entity]:
        """Insert one or more entities"""
        return self._to_entities(conn.execute(self._insert_query(), self._entity_to_dict(instances)))

    def _select(self, conn: Connection, instances: Iterable[Entity]) -> List[Entity]:
        pass
