import click


@click.group('ping')
def ping_group() -> None:
    """Proof of concept"""


@ping_group.command(help='Just checks if the CLI is working')
def ping() -> None:
    click.echo('Pong')

