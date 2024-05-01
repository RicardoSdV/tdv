from typing import Dict

from tdv.domain.entities.atomic_entities.account_entity import Account
from tdv.domain.entities.atomic_entities.portfolio_entity import Portfolio


class Session:
    __slots__ = ('id', 'account', 'portfolios_by_name')

    def __init__(self, account: Account, portfolios_by_name: Dict[str, Portfolio]) -> None:
        self.id = str(hash(account.username))
        self.account = account
        self.portfolios_by_name = portfolios_by_name
