from typing import TYPE_CHECKING, List

from tdv.domain.entities.user_entity import User
from tdv.domain.internal.db_interactive_service import DbInteractiveService
from tdv.domain.types import UserId
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.user_repo import UserRepo

logger = LoggerFactory.make_logger(__name__)

class UsersService(DbInteractiveService):
    def __init__(self, db: 'DB', users_repo: 'UserRepo') -> None:
        super().__init__(db, users_repo)

    def create_user(self, username: str, email: str, password: str) -> List[User]:
        logger.debug('Creating user', username=username, email=email, password=password)
        users = [User(username=username, email=email, password=password)]
        users = self._do_db_operation(self._repo.insert, users)
        return users

    def delete_user_by_id(self, user_id: UserId) -> List[User]:
        logger.debug('Deleting user by ID', user_id=user_id)
        users = [User(user_id=user_id)]
        users = self._do_db_operation(self._repo.delete, users)
        return users

    def get_user_by_email_and_password(self, email: str, password: str) -> List[User]:
        logger.debug('Selecting user by email and password', email=email, password=password)
        users = [User(email=email, password=password)]
        users = self._do_db_operation(self._repo.select, users)
        return users

    def update_username(self, username: str, email: str, password: str):
        logger.debug('Updating username', new_username=username, email=email, password=password)
        users = [User(email=email, password=password)]
        params = {'username': username}
        users = self._do_db_operation(self._repo.update, users, params)
        return users
