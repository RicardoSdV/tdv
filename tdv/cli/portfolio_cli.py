from typing import Optional

from click import group, option, Choice

from tdv.domain.entities.ticker_entity import Tickers
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('portfolio')
def portfolios_group() -> None:
    """Portfolio related operations."""


@portfolios_group.command()
def create() -> None:
    """Creates portfolio for current user"""

    from tdv.containers import Service

    result = Service.portfolio().create_portfolio()
    logger.info('Portfolio created', result=result)


# @portfolios_group.command()
# @option('-p', '--portfolio_id', 'portfolio_id', required=True)
# @option('-t', '--ticker_name', 'ticker_name', type=Choice(Tickers.to_list()))
# @option(
#     '-s',
#     '--share_type',
#     'share_type',
#     type=Choice(ShareTypes.to_list()),
#     required=False,
# )
# def add_shares(portfolio_id: int, portfolio_shares_id: int, __: Optional[str]) -> None:
#     """Links a portfolio to an entry in portfolio_shares table"""
#
#     from tdv.containers import Services
#
#     result = Services.portfolio().create_portfolio_shares(portfolio_id, portfolio_shares_id)
#     logger.info('Shares added to portfolio', result=result)
#
#
# @portfolios_group.command('delete')
# @option('-p', '--portfolio_id', 'portfolio_id', required=True)
# def delete(portfolio_id: int) -> None:
#     """Deletes an entry in portfolio table"""
#
#     from tdv.containers import Services
#
#     result = Services.portfolio().delete_portfolio(portfolio_id)
#     logger.info('Portfolio deleted', result=result)
