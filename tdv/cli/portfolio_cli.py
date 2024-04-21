from click import group, option

from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('portfolios')
def portfolios_group() -> None:
    """Portfolio related operations."""


@portfolios_group.command('create')
@option('-u', '--user_id', 'user_id', required=True)
@option('-c', '--cash', 'cash', required=True)
def create(user_id: int, cash: float) -> None:
    """Creates an entry in portfolio table"""

    from tdv.containers import Services
    result = Services.portfolios().create_portfolio(user_id, cash)
    logger.info('Portfolio created', result=result)


@portfolios_group.command('create-shares')
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
@option('-s', '--portfolio_shares_id', 'portfolio_shares_id', required=True)
def create_shares(portfolio_id: int, portfolio_shares_id: int) -> None:
    """Links a portfolio to an entry in portfolio_shares table"""

    from tdv.containers import Services
    result = Services.portfolios().create_portfolio_shares(portfolio_id, portfolio_shares_id)
    logger.info('Portfolio shares created', result=result)


@portfolios_group.command('delete')
@option('-p', '--portfolio_id', 'portfolio_id', required=True)
def delete(portfolio_id: int) -> None:
    """Deletes an entry in portfolio table"""

    from tdv.containers import Services
    result = Services.portfolios().delete_portfolio(portfolio_id)
    logger.info('Portfolio deleted', result=result)
