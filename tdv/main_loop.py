from datetime import datetime
from time import sleep
from typing import Optional, List, Tuple

from pandas import DataFrame, DatetimeIndex, Timestamp
from pandas_market_calendars import MarketCalendar, get_calendar
from pytz import timezone, tzinfo
from schedule import Scheduler, Job

from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy, BaseServiceProxy
from tdv.types import Time, Second, TimeZone, ExchangeName


class MainLoop:
    __work_only_when_market_open = False

    __active_loop_sleep_time: Second = 1
    __passive_loop_sleep_time: Second = 10

    __check_market_status_time: Time = '01:00'  # Must be before market open
    __time_zone_name_NY: TimeZone = 'America/New_York'
    __time_zone_NY: tzinfo = timezone(__time_zone_name_NY)
    __exchange_name_NY: ExchangeName = 'NYSE'

    def __init__(self) -> None:
        self.__scheduler = Scheduler()

        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

        self.__calendar_nyse: MarketCalendar = get_calendar(self.__exchange_name_NY)

        self.__today_ny: Optional[Timestamp] = None
        self.__update_today_timestamp(self.__time_zone_NY)

        is_market_open_today: bool = self.__is_market_open_today()
        market_open, market_close = self.__market_open_and_close_today(self.__calendar_nyse, self.__time_zone_name_NY)
        self.__base_condition_init(is_market_open_today, market_open, market_close)

        self.__market_open_job: Optional[Job] = None
        self.__market_close_job: Optional[Job] = None
        self.__is_market_open_job: Job = self.__schedule_market_open_and_close_schedules(self.__time_zone_name_NY)

    def __base_condition_init(self, is_market_open_today: bool, market_open: datetime, market_close: datetime) -> None:
        if is_market_open_today:
            now = datetime.now(tz=self.__time_zone_NY)
            if market_open.time() <= now.time() <= market_close.time():
                self.__instantiate_market_dependant_services()
            elif now < market_open:
                self.__schedule_market_open_job(market_open, self.__time_zone_NY)

    def run(self) -> None:
        while True:
            try:
                self.__scheduler.run_pending()  # Run main loop Jobs
                for service in self.__market_dependant_service_proxies:
                    service.run_pending()
                sleep(self.__active_loop_sleep_time)
            except Exception as e:
                print(e)

    def __active_loop(self) -> None:
        pass

    def __passive_loop(self) -> None:
        pass

    def __schedule_market_open_and_close_schedules(self, time_zone: tzinfo) -> Job:
        return self.__scheduler.every().day.at(self.__check_market_status_time, time_zone).do(
            self.__schedule_market_open_and_close_jobs
        )

    def __schedule_market_open_job(self, open_time: datetime, time_zone: tzinfo) -> Job:
        return self.__scheduler.every().day.at(open_time, time_zone).do(
            self.__instantiate_market_dependant_services
        )

    def __schedule_market_close_job(self, close_time: datetime, time_zone: tzinfo) -> Job:
        return self.__scheduler.every().day.at(close_time, time_zone).do(
            self.__delete_all_market_dependant_services
        )

    def __schedule_market_open_and_close_jobs(self) -> Tuple[Job, Job]:
        time_zone = self.__time_zone_name_NY
        self.__update_today_timestamp(time_zone)
        if self.__is_market_open_today():
            market_open, market_close = self.__market_open_and_close_today(
                self.__calendar_nyse, self.__time_zone_name_NY)
            return (self.__schedule_market_open_job(market_open, time_zone),
                    self.__schedule_market_close_job(market_close, time_zone))

    def __instantiate_market_dependant_services(self) -> None:
        """ Instantiate all market dependant services here """
        self.__market_dependant_service_proxies.append(
            YFserviceProxy()
        )

    def __delete_all_market_dependant_services(self) -> None:
        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

    def __is_market_open_today(self) -> bool:
        today = self.__today_ny
        valid_days: DatetimeIndex = self.__calendar_nyse.valid_days(today, today, self.__time_zone_name_NY)
        return today.month == valid_days[0].month and today.day == valid_days[0].day

    def __market_open_and_close_today(self, calendar: MarketCalendar, time_zone: TimeZone) -> Tuple[datetime, datetime]:
        schedule: DataFrame = calendar.schedule(self.__today_ny, self.__today_ny, tz=time_zone)

        market_open, market_close = str(schedule['market_open'][0]), str(schedule['market_close'][0])

        return (datetime.strptime(market_open[:market_open.rfind("-")], '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(market_close[:market_close.rfind("-")], '%Y-%m-%d %H:%M:%S'))

    def __update_today_timestamp(self, time_zone: timezone) -> None:
        self.__today_ny = Timestamp(datetime.now().astimezone(time_zone))
