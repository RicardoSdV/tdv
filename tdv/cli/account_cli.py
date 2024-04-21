from typing import Optional

from click import group, option

from tdv.domain.types import UserId
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('account')
def account_group() -> None:
    """Account related operations."""


@account_group.command()
@option('-u', '--username', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def create(username: str, email: str, password: str) -> None:
    """Create an account"""
    from tdv.containers import Services
    result = Services.users().create_account(username, email, password)
    logger.info('Account created', result=result)


@account_group.command()
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def get(email: str, password: str) -> None:
    from tdv.containers import Services
    result = Services.users().get_account_by_email_and_password(email, password)
    logger.info('Account selected', result=result)


@account_group.command()
@option('-u', '--username_new', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def update(username: str, email: str, password: str) -> None:
    from tdv.containers import Services
    result = Services.users().update_username(username, email, password)
    logger.info('Account updated', result=result)


@account_group.command()
@option('-e', '--email', 'email', required=False)
@option('-p', '--password', 'password', required=False)
def delete(email: Optional[str], password: Optional[str], user_id: Optional[UserId]) -> None:
    """ Delete account by email and password """

    from tdv.containers import Services

    if user_id:
        result = Services.users().delete_account_by_id(user_id)
    elif email:
        raise NotImplementedError()
    elif username:
        raise NotImplementedError()
    else:
        result = None
        logger.error('Must pass at least one arg to get exchange')

    logger.info('Account deleted', result=result)


@account_group.command()
@option('-i', '--id', 'account_id', required=True)
def delete_by_id(account_id: int) -> None:
    """ Delete account by ID """

    from tdv.containers import Services

    if user_id:
        result = Services.users().delete_account_by_id(user_id)
    elif email:
        raise NotImplementedError()
    elif username:
        raise NotImplementedError()
    else:
        result = None
        logger.error('Must pass at least one arg to get exchange')

    logger.info('Account deleted', result=result)
