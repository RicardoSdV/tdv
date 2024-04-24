from typing import TYPE_CHECKING, List, Dict

from tdv.domain.entities.account_entity import Account
from tdv.domain.types import UserId
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.account_repo import AccountRepo

logger = LoggerFactory.make_logger(__name__)


class AccountService:
    def __init__(self, db: 'DB', users_repo: 'AccountRepo') -> None:
        self.db = db
        self.users_repo = users_repo

    def create_account(self, username: str, email: str, password: str) -> List[Account]:
        logger.debug('Creating user', username=username, email=email, password=password)
        users = [Account(username=username, email=email, password=password)]

        with self.db.connect as conn:
            users = self.users_repo.insert(conn, users)
            conn.commit()

        return users

    def delete_account_by_id(self, user_id: UserId) -> List[Account]:
        logger.debug('Deleting user by ID', user_id=user_id)
        users = [Account(user_id=user_id)]

        with self.db.connect as conn:
            users = self.users_repo.delete(conn, users)
            conn.commit()

        return users

    def get_account_by_email_and_password(self, email: str, password: str) -> List[Account]:
        logger.debug('Selecting user by email and password', email=email, password=password)
        users = [Account(email=email, password=password)]

        with self.db.connect as conn:
            result = self.users_repo.select(conn, users)
            conn.commit()

        return result

    def get_account_by_username_and_password(self, username: str, password: str) -> List[Account]:
        logger.debug('Selecting user by username and password', email=username, password=password)
        users = [Account(email=username, password=password)]

        with self.db.connect as conn:
            result = self.users_repo.select(conn, users)
            conn.commit()

        return result

    def update_username(self, username: str, email: str, password: str) -> List[Account]:
        logger.debug('Updating username', new_username=username, email=email, password=password)
        users = [Account(email=email, password=password)]
        params = {'username': username}

        with self.db.connect as conn:
            result = self.users_repo.update(conn, users, params)
            conn.commit()

        return result
