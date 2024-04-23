from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tdv.domain.internal.account_service import AccountService


class SessionService:
    def __init__(self, account_service: 'AccountService') -> None:
        self.account_service = account_service
        self.current_session_user_id: Optional[int] = None

    def login(self, username: str, password: str) -> None:
        accounts = self.account_service.get_account_by_username_and_password(username, password)
        self.current_session_user_id = accounts[0].id

    def logout(self) -> None:
        self.current_session_user_id = None
