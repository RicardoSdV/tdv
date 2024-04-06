from typing import Optional

from click import group, option

from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('user-options')
def user_options_group() -> None:
    """User options table related operations."""


@user_options_group.command('create')
@option('-u', '--user_id', 'user_id', required=True)
@option('-o', '--option_id', 'option_id', required=True)
@option('-c', '--count', 'count', required=False, default=None)
def create(user_id: int, option_id: int, count: Optional[float]) -> None:
    """Creates entry in user_options table"""

    from tdv.containers import Services
    result = Services.user_options().create_user_options(user_id, option_id, count)
    logger.info('Users options created', result=result)
