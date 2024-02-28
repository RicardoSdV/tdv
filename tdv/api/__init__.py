from typing import Optional, TYPE_CHECKING, Dict

from tdv.api.base_resource import BaseResource

if TYPE_CHECKING:
    from tdv.api.ping_resource import PingResource
    from tdv.api.exchanges_resource import ExchangesBaseResource


class Resources:
    def __init__(self) -> None:
        self.__resources: Optional[Dict[str, BaseResource]] = None

        self.__ping_resource: Optional['PingResource'] = None
        self.__exchanges_resource: Optional['ExchangesBaseResource'] = None

    @property
    def routes(self) -> Dict[str, BaseResource]:
        if self.__resources is None:
            self.__resources = {
                '/ping': self.ping_resource,
                '/exchanges_resource': self.exchanges_resource,
            }
        return self.__resources

    @property
    def ping_resource(self) -> 'PingResource':
        if self.__ping_resource is None:
            from tdv.api.ping_resource import PingResource

            self.__ping_resource = PingResource()
        return self.__ping_resource

    @property
    def exchanges_resource(self) -> 'ExchangesBaseResource':
        if self.__exchanges_resource is None:
            from tdv.api.exchanges_resource import ExchangesBaseResource

            self.__exchanges_resource = ExchangesBaseResource()
        return self.__exchanges_resource


resources = Resources()
