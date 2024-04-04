from click import group

from tdv.cli.exchange_cli import exchanges_group
from tdv.cli.format import format_group
from tdv.cli.run import run_group
from tdv.cli.users_cli import users_group


@group()
def cli_root() -> None:
    """Welcome to the TDV CLI, choose a command group:"""


cli_root.add_command(format_group)
cli_root.add_command(run_group)
cli_root.add_command(exchanges_group)
cli_root.add_command(users_group)
