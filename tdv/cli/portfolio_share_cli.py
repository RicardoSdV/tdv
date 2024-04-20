from typing import Optional

from click import group, option, Choice

from tdv.domain.entities.ticker_entity import Tickers
from tdv.domain.entities.ticker_share_type_entity import ShareTypes
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('portfolio-shares')
def portfolio_shares_group() -> None:
    """User shares table related operations."""


@portfolio_shares_group.command('create')
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
@option('-t', '--ticker', 'ticker', type=Choice(Tickers.to_list()), required=True)
@option('-s', '--ticker_share_type_id', 'ticker_share_type_id', required=True)
@option('-c', '--count', 'count', required=True)
def create(portfolio_id: int, ticker: str, ticker_share_type_id: str, count: Optional[int]) -> None:
    """Creates entry in user_share table"""

    from tdv.containers import Services
    result = Services.portfolio_shares().create(portfolio_id, ticker, ticker_share_type_id, count)
    logger.info('Portfolio shares created', result=result)


@portfolio_shares_group.command('get-all')
@option('-u', '--user_id', 'user_id', required=True)
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
def get_portfolio_shares(user_id: int, portfolio_id: int) -> None:
    """Gets shares in a users portfolio"""

    from tdv.containers import Services
    result = Services.portfolio_shares().get_portfolio_shares_by_user_id_and_portfolio_id(user_id, portfolio_id=portfolio_id)
    logger.info('User shares fetched', result=result)


@portfolio_shares_group.command('update-count')
@option('-u', '--user_id', 'user_id', required=True)
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
@option('-t', '--ticker', 'ticker', type=Choice(Tickers.to_list()), required=True)
@option('-s', '--share_type', 'share_type', type=Choice(ShareTypes.to_list()), required=True)
@option('-c', '--count', 'count', required=True)
def update_count(user_id: int, portfolio_id: int, ticker: str, share_type: str, count: float) -> None:
    """Updates user's share count for a share type for a ticker in a portfolio"""

    from tdv.containers import Services
    result = Services.user_shares().update_count_by_user_id_and_share_type(user_id, portfolio_id, ticker, share_type, count)
    logger.info('Portfolio shares updated', result=result)


@portfolio_shares_group.command('delete')
@option('-u', '--user_id', 'user_id', required=True)
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
def delete(user_id: int, portfolio_id: int) -> None:
    """Deletes entry in user_share table"""

    from tdv.containers import Services
    result = Services.user_shares().delete_user_shares_by_id(user_id, portfolio_id)
    logger.info('User shares deleted', result=result)
