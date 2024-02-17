from functools import cached_property
from typing import TypeVar, Dict, Iterable

from sqlalchemy import CursorResult, Insert, Table, Connection, Row

Instance = TypeVar('Instance', bound=object)


class BaseSerializer:
    def _to_instance(self, record: Row):
        """Turn Row objects into domain.entities instances"""
        raise NotImplementedError()

    def _to_dict(self, instance: Instance) -> Dict:
        """Turn domain.entities into dicts by overriding this method"""
        raise NotImplementedError()

    def _for_insert_dict(self, instance: Instance) -> Dict:
        """Override for specific insert dict"""
        return self._to_dict(instance)

    def _for_update_dict(self, instance: Instance) -> Dict:
        """Override for specific update dict"""
        return self._to_dict(instance)


class BaseQueryBuilder:
    @cached_property
    def _table(self) -> Table:
        raise NotImplementedError()

    def _insert_query(self) -> Insert:
        return self._table.insert()


class BaseRepo(BaseQueryBuilder, BaseSerializer):
    def _insert(self, conn: Connection, instance: Instance) -> CursorResult:
        params = self._for_insert_dict(instance)
        query = self._insert_query()
        return conn.execute(query, params)

    def _insert_many(self, conn: Connection, instances: Iterable[Instance]) -> CursorResult:
        params = [self._for_insert_dict(instance) for instance in instances]
        query = self._insert_query()
        return conn.execute(query, params)
