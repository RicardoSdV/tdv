import os
from typing import TYPE_CHECKING

from gunicorn.app.base import BaseApplication


if TYPE_CHECKING:
    from typing import *
    import falcon

    from tdv.libs.log import Logger



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

    def __init__(self, falcon_app: 'falcon.App', logger: 'Logger') -> None:

        self.falcon_app = falcon_app

        self.__logger = logger

        super().__init__()

    def load_config(self) -> None:
        config = {}

        for name, setting in self.options.items():
            if name in self.cfg.settings and setting is not None:
                config[name] = setting
            else:
                self.__logger.error('Bad setting for gunicorn', name=name, setting=setting)

        for name, setting in config.items():
            self.cfg.set(name.lower(), setting)

    def load(self):
        return self.falcon_app
