from click import group, option

from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('acc')
def account_group() -> None:
    """Account related operations."""


@account_group.command()
@option('-u', '--username', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def create(username: str, email: str, password: str) -> None:
    """Create an account"""

    from tdv.containers import Service

    result = Service.account().create_account(username, email, password)
    logger.info('Account created', result=result)


@account_group.command()
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def get(email: str, password: str) -> None:
    """Get account entity by email and password"""

    from tdv.containers import Service

    result = Service.account().get_account_by_email_and_password(email, password)
    logger.info('Account selected', result=result)


@account_group.command()
@option('-u', '--username_new', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def update(username: str, email: str, password: str) -> None:
    """Update username by email and password"""

    from tdv.containers import Service

    result = Service.account().update_username(username, email, password)
    logger.info('Accounts updated', result=result)


@account_group.command()
@option('-i', '--id', 'account_id', required=True)
def delete_by_id(account_id: int) -> None:
    """Delete account by ID"""

    from tdv.containers import Service

    result = Service.account().delete_account_by_id(account_id)
    logger.info('Account deleted', result=result)


@account_group.command()
@option('-u', '--username', 'username', required=True)
@option('-p', '--password', 'password', required=True)
def login(username: str, password: str) -> None:
    """login to an account"""

    from tdv.containers import Service

    session_id = Service.session_manager().login(username, password)
    logger.info('Account login', session_id=session_id)
