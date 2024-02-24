from wsgiref import simple_server

from falcon import Request, Response, HTTP_200, App

from tdv.domain.internal import services


class PingResource:
    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        resp.media = {'message': 'Pong'}

class ExchangesResource:
    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        exchanges = services.exchange_service.get_usd_exchanges()

        response = {}
        for exchange in exchanges:
            exchange_str = repr(exchange)
            response[exchange.__name__] = exchange_str

        resp.media = response

def create_app():
    api = App()
    ping_resource = PingResource()
    ex_res = ExchangesResource()
    api.add_route('/ping', ping_resource)
    api.add_route('/exchanges', ex_res)


    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    print("Serving on http://127.0.0.1:8000")
    httpd.serve_forever()
