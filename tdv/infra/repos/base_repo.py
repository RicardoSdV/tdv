from collections import defaultdict
from functools import cached_property
from typing import Dict, Iterable, Tuple, List, Type, Union, Any

from sqlalchemy import CursorResult, Insert, Table, Connection, Select, ColumnElement, Column, and_, bindparam, Row, \
    Update, Delete

from tdv.domain.entities.base_entity import Entity


class BaseSerializer:
    @cached_property
    def _Entity(self) -> Type[Entity]:
        """Must override with the domain/entities entity that belongs to the overriding subclass"""
        raise NotImplementedError()

    def _to_entities(self, result: CursorResult) -> List[Entity]:
        """Turn Row objects into domain/entities, must pass all params positionally"""
        return [self._Entity(*row) for row in result.fetchall()]

    def _entities_to_dict(self, entities: Iterable[Entity]) -> List[Dict[str, Any]]:
        """Turns domain/entities into param dicts of not None params"""
        params = []
        for entity in entities:
            params.append(self._entity_to_dict(entity))
        return params

    def _row_to_dict(self, row: Row) -> Dict:
        return {name: element for name, element in zip(self._Entity.__slots__, row)}

    @staticmethod
    def _entity_to_dict(entity: Entity) -> Dict[str, Any]:
        params = {}
        for attr_name in entity.__slots__:
            attr = getattr(entity, attr_name)
            if attr is not None:
                params[attr_name] = attr
        return params


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

    def _returning_all(self, query: Union[Insert, Select, Update, Delete]) -> Union[Insert, Select, Update, Delete]:
        return query.returning(self._table)

    @staticmethod
    def _make_for_update(query: Select, key_share: bool = True) -> Select:
        return query.with_for_update(key_share=key_share)


class BaseRepo(BaseQueryBuilder, BaseSerializer):
    def insert(self, conn: Connection, instances: Iterable[Entity]) -> List[Entity]:
        """Insert one or more entities"""
        query = self._returning_all(self._insert_query())
        params = self._entities_to_dict(instances)
        result = conn.execute(query, params)
        result_entities = self._to_entities(result)

        return result_entities

    def select(self, conn: Connection, instances: Iterable[Entity]) -> List[Entity]:
        pass
