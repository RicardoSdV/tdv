from typing import TYPE_CHECKING

from falcon import App

if TYPE_CHECKING:
    from typing import *
    from tdv.libs.log import Logger


class FalconApp(App):
    def __init__(self, resources, logger: 'Logger', *args: 'Any', **kwargs: 'Any') -> None:
        super().__init__(*args, **kwargs)

        for resource in resources:
            self.add_route(resource.route, resource)
