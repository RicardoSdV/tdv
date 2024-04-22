"""
This base repo is designed to be very easy to use, not efficient. As long as child repos override _Entity
and def _table properly, and the Entity is well-defined, Insert, Select, Update, Upsert & Delete queries
should be fully functional out of the box. As to how, look at the available examples.
"""
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import cached_property
from typing import (
    Dict,
    Iterable,
    Tuple,
    List,
    Type,
    TypeVar,
    Generic,
    ClassVar,
    Callable,
)

from sqlalchemy import (
    CursorResult,
    Insert,
    Table,
    Connection,
    Select,
    ColumnElement,
    Column,
    and_,
    bindparam,
    Row,
    tuple_,
    Delete,
    Update,
)

from tdv.domain.entities.base_entity import Entity
from tdv.domain.types import (
    Insertable,
    AttrName,
    NoReturnQuery,
    WhereAbleQuery,
    Insertabless,
)

EntityT = TypeVar('EntityT', bound=Entity)


class BaseSerializer:
    _Entity: ClassVar[Type[Entity]] = Entity

    def _to_entities(self, result: CursorResult) -> List[EntityT]:
        """Turn Row objects into domain/entities, must pass all params positionally"""
        return [self._Entity(*row) for row in result.fetchall()]  # type: ignore

    def _row_to_dict(self, row: Row) -> Dict:
        return {name: element for name, element in zip(self._Entity.__slots__, row)}

    @staticmethod
    def _entities_to_params_dicts(
        entities: Iterable[EntityT],
    ) -> List[Dict[AttrName, Insertable]]:
        """Turns domain/entities into param dicts of not None params"""
        return [entity.to_dict() for entity in entities]

    @staticmethod
    def _entities_to_attrs_list(entities: Iterable[EntityT]) -> Insertabless:
        return [entity.to_list() for entity in entities]

    @staticmethod
    def _entities_to_filters(entities: Iterable[EntityT]) -> Dict[AttrName, List]:
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

    def _delete_query(self) -> Delete:
        return self._table.delete()

    def _update_query(self) -> Update:
        return self._table.update()

    def _any_by_attrs_condition(self, attrs: Insertabless, not_none_slots: List[AttrName]) -> ColumnElement:
        return and_(tuple_(*[c for c in self._all_columns if c.name in not_none_slots]).in_(attrs))

    def _get_by_id_query(self) -> Select:
        return self._select_query().where(self._primary_keys_query)

    def _turn_to_returning_all_query(self, query: NoReturnQuery) -> NoReturnQuery:
        return query.returning(self._table)

    @staticmethod
    def _turn_into_where_query(query: WhereAbleQuery, condition: ColumnElement) -> WhereAbleQuery:
        return query.where(condition)

    @staticmethod
    def _turn_into_for_update_query(query: Select, key_share: bool = True) -> Select:
        return query.with_for_update(key_share=key_share)


class BaseRepo(BaseQueryBuilder, BaseSerializer, Generic[Insertable]):
    def insert(self, conn: Connection, entities: List[EntityT]) -> List[EntityT]:
        query = self._insert_query()
        query = self._turn_to_returning_all_query(query)
        params: List[Dict] = self._entities_to_params_dicts(entities)

        result: CursorResult = conn.execute(query, params)
        entities: List[EntityT] = self._to_entities(result)
        return entities

    def select(self, conn: Connection, entities: List[EntityT], for_update: bool = False) -> List[EntityT]:
        """Generic Select, one or more, returning all, all entities should have the same None attrs"""

        query: Select = self._select_query()
        if for_update:
            query = self._turn_into_for_update_query(query)

        attrs: Insertabless = self._entities_to_attrs_list(entities)
        condition = self._any_by_attrs_condition(attrs, entities[0].not_none_slots())
        query = self._turn_into_where_query(query, condition)

        result = conn.execute(query)
        entities: List[EntityT] = self._to_entities(result)

        return entities

    def update(
        self,
        conn: Connection,
        entities: List[EntityT],
        params: Dict[AttrName, Insertable],
    ) -> List[EntityT]:
        query: Update = self._update_query()
        query = self._turn_to_returning_all_query(query)

        attrs: Insertabless = self._entities_to_attrs_list(entities)
        condition = self._any_by_attrs_condition(attrs, entities[0].not_none_slots())
        query = self._turn_into_where_query(query, condition)

        result = conn.execute(query, params)
        entities: List[EntityT] = self._to_entities(result)

        return entities

    def upsert(self, conn: Connection, entities: List[EntityT]) -> List[EntityT]:
        # TODO
        raise NotImplementedError('Upsert not implemented')

    def delete(self, conn: Connection, entities: List[EntityT]) -> List[EntityT]:
        query: Delete = self._delete_query()
        query = self._turn_to_returning_all_query(query)

        attrs: Insertabless = self._entities_to_attrs_list(entities)
        condition = self._any_by_attrs_condition(attrs, entities[0].not_none_slots())
        query = self._turn_into_where_query(query, condition)

        result = conn.execute(query)
        entities: List[EntityT] = self._to_entities(result)

        return entities
