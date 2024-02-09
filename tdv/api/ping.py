from falcon import Request, Response, HTTP_200, App
from waitress import serve


class PingResource:
    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        resp.media = {'message': 'Pong2'}


def create_app(*args, **kwargs):
    api = App()
    ping_resource = PingResource()
    api.add_route('/ping', ping_resource)

    # Use Waitress to serve the Falcon API
    serve(api, host='127.0.0.1', port=8000)

