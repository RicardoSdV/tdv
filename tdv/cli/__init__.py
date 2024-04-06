from click import group

from tdv.cli.exchange_cli import exchanges_group
from tdv.cli.format import format_group
from tdv.cli.run import run_group
from tdv.cli.ticker_cli import ticker_group
from tdv.cli.ticker_share_types_cli import share_types_group
from tdv.cli.user_options_cli import user_options_group
from tdv.cli.user_shares_cli import user_shares_group
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
cli_root.add_command(user_shares_group)
cli_root.add_command(user_options_group)
