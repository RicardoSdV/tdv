from collections import defaultdict
from functools import cached_property
from typing import Dict, Iterable, Tuple, List, Type, TypeVar

from sqlalchemy import CursorResult, Insert, Table, Connection, Select, ColumnElement, Column, and_, bindparam, Row, \
    tuple_

from tdv.domain.types import Insertable, AttrName, NoReturnQuery

EntityType = TypeVar('EntityType', bound='Entity')

# TODO: Support insert one queries, atm using insert many to insert one


class BaseSerializer:
    @cached_property
    def _Entity(self) -> Type[EntityType]:
        """Must override with the domain/entities entity that belongs to the overriding subclass"""
        raise NotImplementedError()

    def _to_entities(self, result: CursorResult) -> List[EntityType]:
        """Turn Row objects into domain/entities, must pass all params positionally"""
        return [self._Entity(*row) for row in result.fetchall()]

    def _row_to_dict(self, row: Row) -> Dict:
        return {name: element for name, element in zip(self._Entity.__slots__, row)}

    @staticmethod
    def _entities_to_dict(entities: Iterable[EntityType]) -> List[Dict[AttrName, Insertable]]:
        """Turns domain/entities into param dicts of not None params"""
        return [entity.to_dict() for entity in entities]

    @staticmethod
    def _entities_to_attrs_list(entities: Iterable[EntityType]) -> List[List[Insertable]]:
        return [entity.to_list() for entity in entities]

    @staticmethod
    def _entities_to_filters(entities: Iterable[EntityType]) -> Dict[str, List]:
        filters = defaultdict(list)
        for entity in entities:
            for attr_name in entity.__slots__:
                attr = getattr(entity, attr_name)
                if attr is not None:
                    filters[attr_name].append(attr)
        return dict(filters)


class BaseQueryBuilder:
    @cached_property
    def _table(self) -> Table:
        """Must override with the table from database/tables that belongs to the overriding subclass"""
        raise NotImplementedError()

    @cached_property
    def _all_columns(self) -> Tuple[Column, ...]:
        return tuple(column for column in self._table.c)  # Pycharm thinks _table.c isn't iterable, it's wrong.

    @cached_property
    def _primary_key_columns(self) -> Tuple[Column, ...]:
        return tuple(c for c in self._table.c if c.primary_key)

    @cached_property
    def _primary_keys_query(self) -> ColumnElement:
        return and_(*(c == bindparam(f'b_{c.name}') for c in self._primary_key_columns))

    def _insert_query(self) -> Insert:
        return self._table.insert()

    def _select_query(self) -> Select:
        return self._table.select()

    def _any_by_attrs_condition(self, attrs: List[List[Insertable]], not_none_slots: List[AttrName]) -> ColumnElement:
        return and_(tuple_(*[c for c in self._all_columns if c.name in not_none_slots]).in_(attrs))

    def _get_by_id_query(self) -> Select:
        return self._select_query().where(self._primary_keys_query)

    def _turn_to_returning_all_query(self, query: NoReturnQuery) -> NoReturnQuery:
        return query.returning(self._table)

    @staticmethod
    def _turn_into_where_query(query: Select, condition: ColumnElement) -> Select:
        return query.where(condition)

    @staticmethod
    def _turn_into_for_update_query(query: Select, key_share: bool = True) -> Select:
        return query.with_for_update(key_share=key_share)


class BaseRepo(BaseQueryBuilder, BaseSerializer):
    def insert(self, conn: Connection, entities: List[EntityType]) -> List[EntityType]:
        query = self._insert_query()
        query = self._turn_to_returning_all_query(query)
        params: List[Dict] = self._entities_to_dict(entities)

        result: CursorResult = conn.execute(query, params)
        entities: List[EntityType] = self._to_entities(result)
        return entities

    def select(self, conn: Connection, entities: List[EntityType], for_update: bool = False) -> List[EntityType]:
        query: Select = self._select_query()
        if for_update:
            query = self._turn_into_for_update_query(query)

        attrs = self._entities_to_attrs_list(entities)
        condition = self._any_by_attrs_condition(attrs, entities[0].not_none_slots())
        query = self._turn_into_where_query(query, condition)

        result = conn.execute(query)
        entities = self._to_entities(result)

        return entities
