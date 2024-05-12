import os
from typing import TYPE_CHECKING

from gunicorn.app.base import BaseApplication

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    import falcon

logger = LoggerFactory.make_logger(__name__)


class GunicornHTTPServer(BaseApplication):
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 8000))
    workers_amount = 1

    options = {
        'bind': f'{host}:{port}',
        'workers': workers_amount,
        'worker_class': 'gevent',
        'daemon': False,
    }

    def __init__(self, falcon_app: 'falcon.App') -> None:

        self.falcon_app = falcon_app

        super().__init__()

    def load_config(self) -> None:
        config = {}

        for name, setting in self.options.items():
            if name in self.cfg.settings and setting is not None:
                config[name] = setting
            else:
                logger.error('Bad setting for gunicorn', name=name, setting=setting)

        for name, setting in config.items():
            self.cfg.set(name.lower(), setting)

    def load(self):
        return self.falcon_app
