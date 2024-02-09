from wsgiref import simple_server

from falcon import Request, Response, HTTP_200, App


class PingResource:
    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        resp.media = {'message': 'Pong'}


api = App()
ping_resource = PingResource()
api.add_route('/ping', ping_resource)


httpd = simple_server.make_server('127.0.0.1', 8000, api)
print("Serving on http://127.0.0.1:8000")
httpd.serve_forever()
