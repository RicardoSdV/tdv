from typing import Optional

from click import group, option

from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('portfolio-options')
def portfolio_options_group() -> None:
    """User-portfolio options table related operations."""


@portfolio_options_group.command('create')
@option('-u', '--user_id', 'user_id', required=True)
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
@option('-o', '--option_id', 'option_id', required=True)
@option('-c', '--count', 'count', required=False, default=None)
def create(user_id: int, portfolio_id: int, option_id: int, count: Optional[float]) -> None:
    """Creates entry in portfolio_options table"""

    from tdv.containers import Services
    result = Services.user_options().create_portfolio_options(user_id, portfolio_id, option_id, count)
    logger.info('Users options created', result=result)


# @portfolio_options_group.command('get')
# @option('-u', '--user_id', 'user_id', required=True)
# @option('-p', '--portfolio_id', 'portfolio_id', required=True)
# def get_portfolio_options(user_id: int, portfolio_id: int) -> None:
#     """Gets options in a users portfolio"""
#
#     from tdv.containers import Services
#     result = Services.user_options().get_portfolio_options_by_user_id_and_portfolio_id(user_id, portfolio_id)
#     logger.info('Users options fetched', result=result)
#
#
# @portfolio_options_group.command('modify')
# @option('-u', '--user_id', 'user_id', required=True)
# @option('-p', '--portfolio_id', 'portfolio_id', required=True)
# @option('-o', '--option_id', 'option_id', required=True)
# @option('-c', '--count', 'count', required=False, default=None)
# def update_count(user_id: int, portfolio_id: int, option_id: int, count: Optional[float]) -> None:
#     """Modifies entry in portfolio_options table"""
#
#     from tdv.containers import Services
#     result = Services.user_options().modify_portfolio_options(user_id, portfolio_id, option_id, count)
#     logger.info('Users options modified', result=result)
#
#
# @portfolio_options_group.command('delete')
# @option('-u', '--user_id', 'user_id', required=True)
# @option('-p', '--portfolio_id', 'portfolio_id', required=True)
# @option('-o', '--option_id', 'option_id', required=True)
# def delete(user_id: int, portfolio_id: int, option_id: int) -> None:
#     """Deletes entry in portfolio_options table"""
#
#     from tdv.containers import Services
#     result = Services.user_options().delete_portfolio_options(user_id, portfolio_id, option_id)
#     logger.info('Users options deleted', result=result)
