from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.exchnage_ticker_entity import ExchangeTicker
from tdv.infra.database.tables import exchange_ticker_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class ExchangeTickerSerializer(BaseSerializer):
    _Entity: ClassVar[Type[ExchangeTicker]] = ExchangeTicker


class ExchangeTickerQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return exchange_ticker_table


class ExchangeTickerRepo(ExchangeTickerSerializer, ExchangeTickerQueryBuilder, BaseRepo):
    pass
