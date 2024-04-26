from typing import TYPE_CHECKING, Dict

from tdv.domain.session.session import Session

if TYPE_CHECKING:
    from tdv.domain.internal.account_service import AccountService


class SessionManager:
    def __init__(self, account_service: 'AccountService') -> None:
        self.account_service = account_service
        self.sessions: Dict[str, Session] = {}

    def create_session(self, username: str, password: str) -> str:
        accounts = self.account_service.get_account_by_username_and_password(username, password)
        assert len(accounts) == 1
        session = Session(accounts[0])
        self.sessions[session.id] = session
        return session.id
