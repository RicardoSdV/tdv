from collections import defaultdict
from functools import cached_property
from typing import Dict, Iterable, Tuple, List, Type

from sqlalchemy import CursorResult, Insert, Table, Connection, Row, Select, ColumnElement, Column, and_, bindparam

from tdv.domain.entities.entity import Entity


class BaseSerializer:
    @cached_property
    def _Entity(self) -> Type[Entity]:
        """Must override with domain.entities that belongs to the overriding subclass"""
        raise NotImplementedError()

    @cached_property
    def _column_names(self) -> Tuple[str]:
        raise NotImplementedError()

    def _to_entities(self, rows: List[Row]) -> List[Entity]:
        """Turn Row objects into domain.entities with Nones for missing columns"""
        entities = []
        for row in rows:
            entity_attrs = {name: getattr(row, name) for name in row.keys()}
            entities.append(self._Entity(**entity_attrs))
        return entities


    def _to_dict(self, entities: Iterable[Entity]) -> Dict:
        """Turns domain.entities into param dicts of not None params"""
        params = defaultdict(list)
        for entity in entities:
            for attr_name in self._column_names:
                attr = getattr(entity, attr_name)
                if attr is not None:
                    params[f'b_{attr_name}'].append(attr)
        return params

    def _for_insert_dict(self, instance: Entity) -> Dict:
        """Override for specific insert dict"""
        return self._to_dict(instance)

    def _for_update_dict(self, instance: Entity) -> Dict:
        """Override for specific update dict"""
        return self._to_dict(instance)

    @staticmethod
    def _to_dict_of_primary_keys(instances: Iterable[Entity], pk_columns: Iterable[Column]) -> Dict:
        """Might need to override if a table has two primary keys but you want to select by one of them, unlikely"""
        pk_dict = defaultdict(list)
        for instance in instances:
            for column in pk_columns:
                pk_dict[f'b_{column.name}'].append(getattr(instance, column.name))
        return pk_dict


class BaseQueryBuilder:
    @cached_property
    def _table(self) -> Table:
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
    def _insert(self, conn: Connection, instances: Iterable[Entity]) -> CursorResult:
        """Insert one or more instances"""
        params = [self._for_insert_dict(instance) for instance in instances]
        query = self._insert_query()
        return conn.execute(query, params)

    def _get_by_id(self, conn: Connection, instances: Iterable[Entity], for_update: bool = False) -> List[Entity]:
        query = self._select_query()
        if for_update:
            query = self._make_for_update(query)




