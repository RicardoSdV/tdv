from falcon import Request, Response, HTTP_200

from tdv.api.base_resource import BaseResource
from tdv.domain.internal.exchanges_service import ExchangesService


class ExchangesBaseResource(BaseResource):
    def __init__(self, exchange_service: ExchangesService) -> None:
        self.__exchanges_service = exchange_service

    def on_get(self, req: Request, resp: Response):
        resp.status = HTTP_200
        exchanges = self.__exchanges_service.get_usd_exchanges()

        response = {}
        for exchange in exchanges:
            exchange_str = repr(exchange)
            response[exchange.__name__] = exchange_str

        resp.media = response
