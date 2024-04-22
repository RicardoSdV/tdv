from click import group

from tdv.cli.portfolio_cli import portfolios_group
from tdv.cli.run import run_group
from tdv.cli.setup_cli import setup_group
from tdv.cli.account_cli import account_group


@group()
def cli_root() -> None:
    """\b
    TDV CLI is used for:
        - Start & stop services
        - Check system status
        - Mimic API request response as a form of integration testing
        - Automation e.g. fill the DB with mock data for development
        - Config management e.g. change live status for a ticker
    """


cli_root.add_command(run_group)
cli_root.add_command(setup_group)
cli_root.add_command(account_group)
cli_root.add_command(portfolios_group)
