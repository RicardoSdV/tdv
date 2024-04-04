from typing import Optional

from click import group, option

from tdv.domain.types import UserId
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('users')
def users_group() -> None:
    """Users table related operations."""


@users_group.command()
@option('-u', '--username', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def create(username: str, email: str, password: str) -> None:
    from tdv.containers import InternalServices
    result = InternalServices.users_service().create_user(username, email, password)
    logger.info('User created', result=result)


@users_group.command()
@option('-u', '--username', 'username', required=False)
@option('-e', '--email', 'email', required=False)
@option('-i', '--id', 'user_id', required=False)
def delete(username: Optional[str], email: Optional[str], user_id: Optional[UserId]) -> None:
    from tdv.containers import InternalServices

    if user_id:
        result = InternalServices.users_service().delete_user_by_id(user_id)
    elif email:
        raise NotImplementedError()
    elif username:
        raise NotImplementedError()
    else:
        result = None
        logger.error('Must pass at least one arg to get exchange')

    logger.info('User deleted', result=result)


@users_group.command()
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def select(email: str, password: str) -> None:
    from tdv.containers import InternalServices
    result = InternalServices.users_service().get_user_by_email_and_password(email, password)
    logger.info('User selected', result=result)


@users_group.command()
@option('-u', '--username_new', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def update_username(username, email, password):
    from tdv.containers import InternalServices
    result = InternalServices.users_service().update_username(username, email, password)
    logger.info('User updated', result=result)
