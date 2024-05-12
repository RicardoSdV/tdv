from falcon import Request, Response, HTTP_200


class PingResource:
    route = '/ping'

    def on_get(self, req: Request, resp: Response) -> None:
        resp.status = HTTP_200
        resp.media = {'message': 'Pong'}
