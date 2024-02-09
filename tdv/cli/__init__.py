"""CLI Entry point, documentation: http://click.pocoo.org/"""

from os import execv
from subprocess import check_output

import click

from tdv.cli.format import format_group
from tdv.cli.ping import ping_group


@click.group()
def cli_root() -> None:
    pass


@cli_root.command()
def shell() -> None:
    """ ipython shell """
    cmd = check_output(['which', 'ipython']).decode().replace('\n', '')
    execv(cmd, [cmd])


cli_root.add_command(ping_group)
cli_root.add_command(format_group)
