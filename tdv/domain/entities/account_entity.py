from datetime import datetime
from typing import Optional


class Account:
    __slots__ = ('id', 'username', 'email', 'password', 'created_at', 'updated_at')

    def __init__(
        self,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
