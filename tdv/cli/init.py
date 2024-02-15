import click


@click.group('init')
def format_group() -> None:
    """ For automating project setup, environment variable declarations, dependencies etc  """