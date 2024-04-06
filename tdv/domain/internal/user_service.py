from typing import TYPE_CHECKING, List, Dict

from tdv.domain.entities.user_entity import User
from tdv.domain.types import UserId
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.user_repo import UserRepo

logger = LoggerFactory.make_logger(__name__)


class UsersService:
    def __init__(self, db: 'DB', users_repo: 'UserRepo') -> None:
        self.db = db
        self.users_repo = users_repo

    def create_user(self, username: str, email: str, password: str) -> List[User]:
        logger.debug('Creating user', username=username, email=email, password=password)
        users = [User(username=username, email=email, password=password)]

        with self.db.connect as conn:
            users = self.users_repo.insert(conn, users)
            conn.commit()

        return users

    def delete_user_by_id(self, user_id: UserId) -> List[User]:
        logger.debug('Deleting user by ID', user_id=user_id)
        users = [User(user_id=user_id)]

        with self.db.connect as conn:
            users = self.users_repo.delete(conn, users)
            conn.commit()

        return users

    def get_user_by_email_and_password(self, email: str, password: str) -> List[User]:
        logger.debug('Selecting user by email and password', email=email, password=password)
        users = [User(email=email, password=password)]

        with self.db.connect as conn:
            users = self.users_repo.select(conn, users)
            conn.commit()

        return users

    def update_username(self, username: str, email: str, password: str) -> List[User]:
        logger.debug('Updating username', new_username=username, email=email, password=password)
        users = [User(email=email, password=password)]
        params = {'username': username}

        with self.db.connect as conn:
            users = self.users_repo.update(conn, users, params)
            conn.commit()

        return users
