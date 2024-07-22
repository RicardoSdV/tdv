from datetime import datetime
from time import sleep

from tdv.constants import MAIN_LOOP_SLEEP_TIME
from tdv.containers import ExternalService, logger_factory

logger = logger_factory.make_logger('main_loop', override_save_main=False)

class MainLoop:

    @staticmethod
    def run() -> None:

        sleep_time = MAIN_LOOP_SLEEP_TIME

        yahoo_finance_service_proxy = ExternalService.yahoo_finance()

        while True:
            try:
                logger.info(
                    'Loop of the main loop',
                    utctime=datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'),
                    localtime=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                )
                yahoo_finance_service_proxy.run_pending()
                logger_factory.run_pending()

                sleep(sleep_time)
            except Exception as e:
                logger.error('Main loop', exc=e)
