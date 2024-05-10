import os
from typing import Optional, Dict

from falcon import App
from gunicorn.app.base import BaseApplication

from tdv.api import resources


class WebApp(BaseApplication):
    default_host = '0.0.0.0'
    default_port = int(os.environ.get('PORT', 8000))
    default_num_workers = 1

    def __init__(self) -> None:
        super().__init__()
        self.__options: Optional[Dict] = None
        self.__web_app: Optional[App] = None

    @property
    def web_app(self) -> App:
        if self.__web_app is None:
            self.__web_app = App()
        return self.__web_app

    @property
    def default_options(self) -> Dict:
        return {
            'bind': f'{self.default_host}:{self.default_port}',
            'workers': self.default_num_workers,
            'accesslog': '-',
            'errorlog': '-',
            'worker_class': 'gevent',
        }

    def add_routes(self) -> None:
        app = self.web_app
        for route, resource in resources.routes.items():
            app.add_route(route, resource)

    def set_options(self, custom_options: Optional[Dict[str, str]] = None) -> None:
        options = self.default_options if custom_options is None else custom_options

        for option_name, option_value in options.items():
            if option_name in self.cfg.settings and option_value is not None:
                self.cfg.set(option_name.lower(), option_value)
