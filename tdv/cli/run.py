import subprocess

import click


@click.group('run')
def run_group() -> None:
    """Run different services such as Yahoo Finance or the APIs"""


@run_group.command('test')
def test() -> None:
    """ For testing logger """

    from tdv.logger_setup import logger_obj
    logger = logger_obj.get_logger(__name__)
    logger.info('Test message', test_arg='example')


@run_group.command('yf')
def yf() -> None:
    """Run periodic requests to Yahoo Finance to request options data"""
    from tdv.constants import ROOT_DIR_PATH
    from tdv.common_utils import declare_path
    from tdv.run import run

    declare_path(ROOT_DIR_PATH)
    run()


@run_group.command()
def ping() -> None:
    """Runs the ping API on a gunicorn worker"""
    command = [
        'gunicorn',
        '--bind', '0.0.0.0:8000',
        '--workers', '1',
        '--worker-class', 'sync',
        'tdv.api.ping:create_app()'
    ]
    subprocess.run(command)
