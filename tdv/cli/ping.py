import subprocess

import click
import structlog

logger = structlog.get_logger(__name__)


@click.group('ping')
def ping_group() -> None:
    """Proof of concept"""


@ping_group.command(help='Just checks if the CLI is working')
def ping() -> None:
    logger.info('Pong')


@ping_group.command('run', help='Runs the ping API in a gunicorn worker')
def run_for_linux() -> None:
    command = [
        'gunicorn',
        '--bind', '0.0.0.0:8000',
        '--workers', '1',
        '--worker-class', 'sync',
        'tdv.api.ping:create_app()'
    ]
    subprocess.run(command)
