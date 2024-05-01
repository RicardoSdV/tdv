from typing import ClassVar, Type

from sqlalchemy import Table

from tdv.domain.entities.account_entity import Account
from tdv.infra.database.tables import account_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo


class AccountSerializer(BaseSerializer):
    _Entity: ClassVar[Type[Account]] = Account


class AccountQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> Table:
        return account_table


class AccountRepo(AccountSerializer, AccountQueryBuilder, BaseRepo):
    pass
