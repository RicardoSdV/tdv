import subprocess

import click


@click.group('ping')
def ping_group() -> None:
    """Proof of concept"""


@ping_group.command(help='Just checks if the CLI is working')
def ping() -> None:
    click.echo('Pong')


@ping_group.command('lin_run', help='Runs the ping API in a gunicorn worker')
def run_for_linux() -> None:
    command = [
        'gunicorn',
        '--bind', '0.0.0.0:8000',
        '--workers', '1',
        '--worker-class', 'sync',
        'tdv.api.ping:create_app()'
    ]
    subprocess.run(command)


@ping_group.command('win_run', help='Runs the ping API in a waitress worker')
def run_for_windows():
    command = [
        'waitress-serve',
        '--listen=0.0.0.0:8000',
        'tdv.api.ping:create_app'
    ]
    subprocess.run(command)
