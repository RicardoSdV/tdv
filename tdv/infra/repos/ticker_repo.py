from functools import cached_property
from typing import Type

from sqlalchemy import Table

from tdv.domain.entities.ticker_entity import Ticker
from tdv.infra.database.tables import tickers_table
from tdv.infra.repos.base_repo import BaseRepo


class TickerSerializer:
    @cached_property
    def _Entity(self) -> Type[Ticker]:
        return Ticker


class TickerQueryBuilder:
    @property
    def _table(self) -> Table:
        return tickers_table


class TickerRepo(TickerSerializer, TickerQueryBuilder, BaseRepo):
    pass
