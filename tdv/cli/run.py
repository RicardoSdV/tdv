from click import group
from gevent import subprocess

from tdv.containers import logger_factory

logger = logger_factory.make_logger('cli')

@group('run')
def run_group() -> None:
    """Run different services such as Yahoo Finance or the APIs"""


@run_group.command()
def log() -> None:
    """For testing logger"""
    logger.info('Test message', test_arg='example')


@run_group.command()
def yf() -> None:
    """Run periodic requests to Yahoo Finance to request options data & save in DB"""

    import sys

    from tdv.containers import Service
    from tdv.constants import PATH
    from tdv.run import run

    Service.cache_manager().init_entity_cache()
    sys.path.append(str(PATH.DIR.ROOT))
    run()


@run_group.command()
def web() -> None:
    from tdv.containers import API

    win_host = subprocess.check_output(['hostname', '-I']).decode('utf-8').strip()
    logger.info('If using WSL visit', url=f'http://{win_host}:8000')

    API.gunicorn_server().run()
