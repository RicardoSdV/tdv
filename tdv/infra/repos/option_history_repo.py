from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.option_history_entity import OptionHistory
from tdv.infra.database.tables import option_history_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class OptionHistorySerializer(BaseSerializer):
    _Entity: ClassVar[Type[OptionHistory]] = OptionHistory


class OptionHistoryQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return option_history_table


class OptionHistoryRepo(OptionHistorySerializer, OptionHistoryQueryBuilder, BaseRepo):
    pass
