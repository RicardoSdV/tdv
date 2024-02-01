from time import sleep

import schedule

from tdv.common_utils import timestamp
from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy


class MainLoop:
    # Settings (all times in seconds)
    __update_tesla_exp_time = 10
    __main_loop_sleep_time = 1

    def __init__(self) -> None:
        # Services
        self.__yf_service = YFserviceProxy()

        # Events scheduling
        self.__schedule_update_events()

    def run(self) -> None:
        cnt = 0
        sleep_time = self.__main_loop_sleep_time
        while True:
            try:
                schedule.run_pending()
                self.__yf_service.call_saves()
            except Exception as e:
                print(e, '\nThis exception happened at:', timestamp())
            sleep(sleep_time)
            cnt += 1
            print('Loops cnt:', cnt)

    def __schedule_update_events(self) -> None:
        schedule.every(self.__update_tesla_exp_time).seconds.do(self.__yf_service.call_updates)
