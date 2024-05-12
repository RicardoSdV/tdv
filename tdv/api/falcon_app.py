from falcon import App

from tdv.domain.types import Args, KwArgs


class FalconApp(App):
    def __init__(self, resources, *args: Args, **kwargs: KwArgs) -> None:
        super().__init__(*args, **kwargs)

        for resource in resources:
            self.add_route(resource.route, resource)
