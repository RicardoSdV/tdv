from falcon import Request, Response, HTTP_200

from tdv.api.base_resource import BaseResource


class PingResource(BaseResource):
    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        resp.media = {'message': 'Pong'}
