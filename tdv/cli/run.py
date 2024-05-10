from click import group

from tdv.api.web_app import WebApp
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


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


# @run_group.command()
# def ping() -> None:
#     """Runs the ping API on a gunicorn worker"""
#
#
#     web_app = WebApp.web_app
#
#     # Add routes to the web app
#     web_app.add_routes()
#     web_app.set_options()
#
#     # Construct the command to run Gunicorn
#     command = [
#         'gunicorn',
#         f"--bind={web_app.default_host}",
#         f"--workers={web_app.de}",
#         f"--worker-class={custom_options['worker_class']}",
#         'tdv.api.ping:create_app()',
#     ]
#
#     # Run Gunicorn using subprocess
#     subprocess.run(command)
