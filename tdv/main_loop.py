from time import sleep

from tdv.constants import MAIN_LOOP_SLEEP_TIME
from tdv.containers import ExternalService
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class MainLoop:
    @staticmethod
    def run() -> None:

        sleep_time = MAIN_LOOP_SLEEP_TIME

        yahoo_finance_service_proxy = ExternalService.yahoo_finance()

        while True:
            try:
                print('yes')
                yahoo_finance_service_proxy.run_pending()

                sleep(sleep_time)
            except Exception as e:
                logger.exception('Main loop', exc=e)
