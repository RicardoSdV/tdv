from functools import cached_property
from typing import Type

from sqlalchemy import Table

from tdv.domain.entities.account_entity import Account
from tdv.infra.database.tables import account_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class AccountSerializer(BaseSerializer):
    _Entity = Account


class AccountQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return account_table


class UserRepo(AccountSerializer, AccountQueryBuilder, BaseRepo):
    pass
