from click import group, option, Choice

from tdv.domain.entities.ticker_entity import TickersEnum
from tdv.domain.entities.ticker_share_type_entity import ShareTypes
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('user-shares')
def user_shares_group() -> None:
    """User shares table related operations."""


@user_shares_group.command('create')
@option('-u', '--user_id', 'user_id', required=True)
@option('-t', '--ticker_share_type_id', 'ticker_share_type_id', required=True)
@option('-c', '--count', 'count', required=False, default=None)
def create(user_id: int, ticker_share_type_id: int, count: int) -> None:
    """Creates entry in user_share table"""

    from tdv.containers import Services
    result = Services.user_shares().create_user_shares(user_id, ticker_share_type_id, count)
    logger.info('Users shares created', result=result)


@user_shares_group.command('delete')
@option('-i', '--user_shares_id', 'user_shares_id', required=True)
def delete(user_shares_id: int) -> None:
    """Deletes entry in user_share table"""

    from tdv.containers import Services
    result = Services.user_shares().delete_user_shares_by_id(user_shares_id)
    logger.info('User shares deleted', result=result)


@user_shares_group.command('update-count')
@option('-i', '--user_id', 'user_id', required=True)
@option('-t', '--ticker', 'ticker', type=Choice(TickersEnum.to_list()), required=True)
@option('-s', '--share_type', 'share_type', type=Choice(ShareTypes.to_list()), required=True)
@option('-c', '--count', 'count', required=True)
def update_count(user_id: int, ticker: str, share_type: str, count: float) -> None:
    """Updates user's share count for a share type for a ticker in user_shares table"""

    from tdv.containers import Services
    result = Services.user_shares().update_count_by_user_id_and_share_type(user_id, ticker, share_type, count)
    logger.info('User shares updated', result=result)