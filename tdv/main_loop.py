from time import sleep
from typing import List

from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy, BaseServiceProxy
from tdv.domain.types import Second
from tdv.logger_setup import logger_factory

logger = logger_factory.make_logger(__name__)


class MainLoop:
    __sleep_time: Second = 1

    def __init__(self) -> None:
        self.__services_with_jobs: List[BaseServiceProxy] = [
            YFserviceProxy(),
        ]

    def run(self) -> None:
        while True:
            try:
                for service in self.__services_with_jobs:
                    service.run_pending()
                sleep(self.__sleep_time)
            except Exception as e:
                logger.exception('Main loop', exc=e)
