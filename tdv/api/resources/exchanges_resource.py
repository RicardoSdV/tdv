from falcon import Request, Response

from tdv.domain.services.independent_services.exchange_service import ExchangeService


class ExchangesBaseResource:
    def __init__(self, exchange_service: ExchangeService) -> None:
        self.__exchanges_service = exchange_service

    def on_get(self, req: Request, resp: Response) -> None:
        print('get')
        # resp.status = HTTP_200
        # exchanges = self.__exchanges_service.get_exchange_by_name(ExchangeAbrvs.NEW_YORK.value)
        #
        # response = {}
        # for exchange in exchanges:
        #     exchange_str = repr(exchange)
        #     response[exchange.name] = exchange_str
        #
        # resp.media = response
