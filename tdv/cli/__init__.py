from click import group

from tdv.cli.portfolio_cli import portfolios_group
from tdv.cli.run import run_group
from tdv.cli.setup_cli import ticker_group
from tdv.cli.account_cli import account_group


"""

Current functionality goals:

Account:
    - Create an account
    - Update username
    - Delete a an account
    - Session: log in once, work with that rather than passing username or something for every operation
    
Portfolio:
    - Create a portfolio
    - Add shares to a portfolio
    - Add options to a portfolio
    - Update portfolio shares
    - Update portfolio options
    - Get all portfolio data
    - Delete a portfolio
    
Ticker:
    - Live / Historical support hybrid: Download options every certain interval & use the last DB insertion as the 
    "live" data to perform analysis.


"""


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
cli_root.add_command(ticker_group)
cli_root.add_command(account_group)
cli_root.add_command(portfolios_group)


"""
Future functionality goals:

Account:
    - Make account secure, passwords etc (use google? way better than handling accounts)

Ticker:
    - Historical support: Have a comprehensive set of options downloaded & perform analysis based on timestamps
    - Live support: Download options and perform analysis without having the options pass through the DB
"""
