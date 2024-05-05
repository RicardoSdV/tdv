from click import group

from tdv.cli.local_user_cli import local_user_group
from tdv.cli.portfolio_cli import portfolio_group
from tdv.cli.run import run_group
from tdv.cli.setup_cli import setup_group
from tdv.cli.account_cli import account_group


@group()
def cli_root() -> None:
    """\b
    TDV CLI is used for:
        - Start & stop services
        - Check system status
        - Mimic API function for testing (local user for example)
        - Automation e.g. fill DB with mock data
        - Config management e.g. change live status for a ticker
    """


cli_root.add_command(run_group)
cli_root.add_command(setup_group)
cli_root.add_command(account_group)
cli_root.add_command(portfolio_group)
cli_root.add_command(local_user_group)
