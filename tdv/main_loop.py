from datetime import datetime as Datetime
from time import sleep
from typing import Optional, List, Tuple, Callable

from pandas import DataFrame, DatetimeIndex, Timestamp
from pandas_market_calendars import MarketCalendar, get_calendar
from pytz import timezone, tzinfo
from schedule import Scheduler, Job

from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy, BaseServiceProxy
from tdv.data_types import Second, ExchangeName


class MainLoop:
    __work_only_when_market_open = False

    __active_loop_sleep_time: Second = 1
    __passive_loop_sleep_time: Second = 10

    __daily_rescheduling_time: Datetime = Datetime.strptime('01:00', '%H:%M')  # Before market open

    __timezone_NY: tzinfo = timezone('America/New_York')
    __exchange_NY: ExchangeName = 'NYSE'

    def __init__(self) -> None:
        self.__scheduler = Scheduler()

        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

        self.__calendar_nyse: MarketCalendar = get_calendar(self.__exchange_NY)

        self.__today_ny: Optional[Timestamp] = None
        self.__update_today_timestamp(self.__timezone_NY)

        is_market_open_today: bool = self.__is_market_open_today()
        market_open, market_close = self.__market_times_today(self.__calendar_nyse, self.__timezone_NY)
        self.__base_condition_init(is_market_open_today, market_open, market_close)

        self.__market_open_job: Optional[Job] = None
        self.__market_close_job: Optional[Job] = None
        self.__is_market_open_ny_job: Job = self.__schedule_daily(
            self.__schedule_market_open_and_close_jobs, self.__daily_rescheduling_time, self.__timezone_NY)

    def run(self) -> None:
        while True:
            try:
                self.__scheduler.run_pending()  # Run main loop Jobs
                for service in self.__market_dependant_service_proxies:
                    service.run_pending()
                sleep(self.__active_loop_sleep_time)
            except Exception as e:
                print(e)

    def __base_condition_init(self, is_market_open_today: bool, market_open: Datetime, market_close: Datetime) -> None:
        if is_market_open_today:
            now = Datetime.now(tz=self.__timezone_NY)
            if market_open <= now <= market_close:  # Open now
                self.__instantiate_ny_services()
                self.__schedule_daily(self.__instantiate_ny_services, market_close, self.__timezone_NY)
            elif now < market_open:  # Open later
                self.__schedule_daily(self.__instantiate_ny_services, market_open, self.__timezone_NY)
                self.__schedule_daily(self.__delete_all_market_dependant_services, market_close, self.__timezone_NY)

    def __instantiate_ny_services(self) -> None:
        """ Instantiate all NY market dependant services here """
        self.__market_dependant_service_proxies.append(
            YFserviceProxy()
        )

    def __delete_all_market_dependant_services(self) -> None:
        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []

    def __schedule_daily(self, method: Callable, time: Datetime, time_zone: tzinfo) -> Job:
        return self.__scheduler.every().day.at(time.strftime('%H:%M'), time_zone).do(method)

    def __schedule_market_open_and_close_jobs(self) -> Tuple[Job, Job]:
        time_zone = self.__timezone_NY
        self.__update_today_timestamp(time_zone)
        if self.__is_market_open_today():
            market_open, market_close = self.__market_times_today(self.__calendar_nyse, time_zone)
            return (self.__schedule_daily(self.__instantiate_ny_services, market_open, time_zone),
                    self.__schedule_daily(self.__delete_all_market_dependant_services, market_close, time_zone))

    def __is_market_open_today(self) -> bool:
        today = self.__today_ny
        valid_days: DatetimeIndex = self.__calendar_nyse.valid_days(today, today, self.__timezone_NY)
        return today.month == valid_days[0].month and today.day == valid_days[0].day

    def __market_times_today(self, calendar: MarketCalendar, time_zone: tzinfo) -> Tuple[Datetime, Datetime]:
        schedule: DataFrame = calendar.schedule(self.__today_ny, self.__today_ny, tz=time_zone)
        return schedule['market_open'][0].to_pydatetime(), schedule['market_close'][0].to_pydatetime()

    def __update_today_timestamp(self, time_zone: timezone) -> None:
        self.__today_ny = Timestamp(Datetime.now().astimezone(time_zone))
