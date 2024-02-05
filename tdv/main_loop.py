from datetime import datetime
from time import sleep
from typing import Optional, List, Tuple

from pandas import DataFrame
from pandas_market_calendars import MarketCalendar, get_calendar
from pytz import timezone
from schedule import Scheduler, Job
import pandas_market_calendars as mcal

from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy, BaseServiceProxy
from tdv.types import Time, Second, TimeZone, ExchangeName, TimeStamp, Date


# Scheduling for market open
# end weekend job -> re-schedule market opening and closing jobs
# market open job -> create all services that need the market to be open
# market close job -> delete all services that need the market to be open
# start weekend job -> de-schedule market opening and closing jobs and delete objects

# Schedule all these jobs on init ^^^^

# Main Loop:
# Run the passive loop until the creation of a service object is appropriate
# If any service objects exist run the active loop
# When running the active loop:
# keep asking whether more service objects have to be created
# After this run the pending jobs in the created services

# DISCLAIMER: This is all happening in one thread, eventually the requests
# should happen in another thread so the request response cycle does not delay
# the creation of more objects but that's pretty complicated


class MainLoop:
    __work_only_when_market_open = False

    __active_loop_sleep_time: Second = 1
    __passive_loop_sleep_time: Second = 10

    __check_market_status_time: Time = '00:01'  # Must be before market open
    __time_zone_NY: TimeZone = 'America/New_York'
    __exchange_name_NY: ExchangeName = 'NYSE'

    def __init__(self) -> None:
        self.__scheduler = Scheduler()

        self.__market_open_job: Optional[Job] = None
        self.__market_close_job: Optional[Job] = None
        self.__is_market_open_job: Job = self.__schedule_market_open_and_close_schedules(self.__time_zone_NY)

        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

        self.__nyse_calendar: MarketCalendar = get_calendar(self.__exchange_name_NY)

        self.__today_ymd_ny: Optional[TimeStamp] = None

    def run(self) -> None:
        while True:
            self.__scheduler.run_pending()  # Run main loop Jobs
            for service in self.__market_dependant_service_proxies:
                service.run_pending()
            sleep(self.__active_loop_sleep_time)

    def __active_loop(self) -> None:
        pass

    def __passive_loop(self) -> None:
        pass

    def __schedule_market_open_and_close_schedules(self, time_zone: TimeZone) -> Job:
        return self.__scheduler.every().day.at(self.__check_market_status_time, time_zone).do(
            self.__schedule_market_open_and_close_jobs()
        )

    def __schedule_market_open_job(self, open_time: Time, time_zone: TimeZone) -> Job:
        return self.__scheduler.every().day.at(open_time, time_zone).do(
            self.__instantiate_market_dependant_services()
        )

    def __schedule_market_close_job(self, close_time: Time, time_zone: TimeZone) -> Job:
        return self.__scheduler.every().day.at(close_time, time_zone).do(
            self.__delete_all_market_dependant_services()
        )

    def __schedule_market_open_and_close_jobs(self, calendar: MarketCalendar, time_zone: TimeZone) -> Tuple[Job, Job]:
        self.__today_timestamp = self.__today_timestamp()
        if self.__is_market_open_today():
            market_open, market_close = self.__get_market_schedule_today(calendar)
            return self.__schedule_market_open_job(market_open, time_zone), self.__schedule_market_close_job(market_close, time_zone)

    def __instantiate_market_dependant_services(self) -> None:
        """ Instantiate all market dependant services here """
        self.__market_dependant_service_proxies.append(
            YFserviceProxy()
        )

    def __delete_all_market_dependant_services(self) -> None:
        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

    def __is_market_open_today(self) -> bool:
        return self.today_timestamp() in self.__nyse_calendar.valid_days

    def __market_open_and_close_today(self, calendar: MarketCalendar, time_zone: TimeZone) -> Tuple[Date, Date]:
        schedule: DataFrame = calendar.schedule(self.__today_ymd_ny, self.__today_ymd_ny, tz=time_zone)
        return schedule.market_open, schedule.market_close

    def __update_today_timestamp(self, time_zone: TimeZone) -> None:
        self.__today_ymd_ny = datetime.now(timezone(time_zone)).strftime('%Y-%m-%d')
