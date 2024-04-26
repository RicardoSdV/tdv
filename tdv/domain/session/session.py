from typing import Optional

from tdv.domain.entities.account_entity import Account


class Session:
    __slots__ = 'id', 'account'

    def __init__(self, account: Account) -> None:
        self.id = str(hash(account.username))
        self.account = account
