from click import group

from tdv.cli.exchange_cli import exchanges_group
from tdv.cli.format import format_group
from tdv.cli.portfolios_cli import portfolios_group
from tdv.cli.run import run_group
from tdv.cli.ticker_cli import ticker_group
from tdv.cli.ticker_share_types_cli import share_types_group
from tdv.cli.portfolio_option_cli import portfolio_options_group
from tdv.cli.portfolio_share_cli import portfolio_shares_group
from tdv.cli.users_cli import users_group


@group()
def cli_root() -> None:
    """Welcome to the TDV CLI, choose a command group:"""


cli_root.add_command(format_group)
cli_root.add_command(run_group)
cli_root.add_command(exchanges_group)
cli_root.add_command(ticker_group)
cli_root.add_command(users_group)
cli_root.add_command(share_types_group)
cli_root.add_command(portfolio_shares_group)
cli_root.add_command(portfolio_options_group)
cli_root.add_command(portfolios_group)
