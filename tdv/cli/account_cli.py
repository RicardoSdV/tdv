from click import group, option

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

    result = Services.account().create_account(username, email, password)
    logger.info('Account created', result=result)


@account_group.command()
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def get(email: str, password: str) -> None:
    """Get account entity by email and password"""

    from tdv.containers import Services

    result = Services.account().get_account_by_email_and_password(email, password)
    logger.info('Account selected', result=result)


@account_group.command()
@option('-u', '--username_new', 'username', required=True)
@option('-e', '--email', 'email', required=True)
@option('-p', '--password', 'password', required=True)
def update(username: str, email: str, password: str) -> None:
    """Update username by email and password"""

    from tdv.containers import Services

    result = Services.account().update_username(username, email, password)
    logger.info('Accounts updated', result=result)


@account_group.command()
@option('-i', '--id', 'account_id', required=True)
def delete_by_id(account_id: int) -> None:
    """Delete account by ID"""

    from tdv.containers import Services

    result = Services.account().delete_account_by_id(account_id)
    logger.info('Account deleted', result=result)


@account_group.command()
@option('-u', '--username', 'username', required=True)
@option('-p', '--password', 'password', required=True)
def login(username: str, password: str) -> None:
    """login to an account"""

    from tdv.containers import Services

    result = Services.session().login(username, password)
    logger.info('Account created', result=result)
