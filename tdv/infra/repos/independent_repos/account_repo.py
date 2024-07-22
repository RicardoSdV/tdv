from typing import TYPE_CHECKING

from tdv.domain.entities.independent_entities.account_entity import Account
from tdv.infra.database.tables.independent_tables import account_table
from tdv.infra.repos.base_repo import BaseSerializer, BaseQueryBuilder, BaseRepo

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *


class AccountSerializer(BaseSerializer):
    _Entity: 'ClassVar[Type[Account]]' = Account


class AccountQueryBuilder(BaseQueryBuilder):
    @property
    def _table(self) -> 'Table':
        return account_table


class AccountRepo(AccountSerializer, AccountQueryBuilder, BaseRepo):
    pass
