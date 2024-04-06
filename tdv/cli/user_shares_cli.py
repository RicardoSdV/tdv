from click import group, option

from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('user-shares')
def user_shares_group() -> None:
    """User shares table related operations."""


@user_shares_group.command()
@option('-u', '--user_id', 'user_id', required=True)
@option('-t', '--ticker_share_type_id', 'ticker_share_type_id', required=True)
@option('-c', '--count', 'count', required=False, default=None)
def create(user_id: int, ticker_share_type_id: int, count: int) -> None:
    """Creates entry in user_share table"""

    from tdv.containers import Services
    result = Services.user_shares().create_user_share(user_id, ticker_share_type_id, count)
    logger.info('Users shares created', result=result)
