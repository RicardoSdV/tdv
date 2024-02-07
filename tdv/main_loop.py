from datetime import datetime as Datetime
from time import sleep
from typing import Optional, List, Tuple, Callable

from pandas import DataFrame, DatetimeIndex, Timestamp
from pandas_market_calendars import MarketCalendar, get_calendar
from pytz import timezone, tzinfo
from schedule import Scheduler, Job

from tdv.domain.external.yahoo_finance_service_proxy import YFserviceProxy, BaseServiceProxy
from tdv.data_types import Second, ExchangeName
from tdv.logger_settup import tdv_logger


class MainLoop:
    __work_only_when_market_open = False

    __active_loop_sleep_time: Second = 1
    __passive_loop_sleep_time: Second = 10

    __daily_rescheduling_time: Datetime = Datetime.strptime('01:00', '%H:%M')  # Before market open

    __timezone_NY: tzinfo = timezone('America/New_York')
    __exchange_NY: ExchangeName = 'NYSE'

    tdv_logger.info("Main Loop instantiated")

    def __init__(self) -> None:
        self.__scheduler = Scheduler()
        tdv_logger.info("Job scheduler instantiated")

        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []
        tdv_logger.info("Market dependant job list created")

        self.__calendar_nyse: MarketCalendar = get_calendar(self.__exchange_NY)
        tdv_logger.info("Market calendar fetched")

        self.__today_ny: Optional[Timestamp] = None
        self.__update_today_timestamp(self.__timezone_NY)
        tdv_logger.info("Time in NY checked")

        is_market_open_today: bool = self.__is_market_open_today()
        tdv_logger.info("Market status checked")
        market_open, market_close = self.__market_times_today(self.__calendar_nyse, self.__timezone_NY)
        tdv_logger.info("Market open and close times checked for last time market was open"
                        "")

        self.__base_condition_init(is_market_open_today, market_open, market_close)

        # Creo que esta seción está mal
        self.__market_open_job: Optional[Job] = None
        self.__market_close_job: Optional[Job] = None
        self.__is_market_open_ny_job: Job = self.__schedule_daily(
            self.__schedule_market_open_and_close_jobs, self.__daily_rescheduling_time, self.__timezone_NY) # aquí calleamos __schedule_market_open_and_close_jobs, go there

    def run(self) -> None:
        tdv_logger.info("Entering infinite loop now.")
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
            tdv_logger.info("Market is open, checking exact time now")
            if market_open <= now <= market_close:
                tdv_logger.info("Market is open right now")
                self.__instantiate_ny_services()
                self.__schedule_daily(self.__instantiate_ny_services, market_close, self.__timezone_NY)
                tdv_logger.info("FserciceProxy job scheduled to stop at market close")
            elif now < market_open:  # Open later
                tdv_logger.info("The market is not yet open today")
                self.__schedule_daily(self.__instantiate_ny_services, market_open, self.__timezone_NY)
                tdv_logger.info("FserciceProxy job scheduled to start at market open")
                self.__schedule_daily(self.__delete_all_market_dependant_services, market_close, self.__timezone_NY)
                tdv_logger.info("FserciceProxy job scheduled to stop at market close")
            else:
                tdv_logger.info("The market closed for today")
        else:
            tdv_logger.info("The market does not open today")

    def __instantiate_ny_services(self) -> None:
        """ Instantiate all NY market dependant services here """
        self.__market_dependant_service_proxies.append(
            YFserviceProxy()
        )
        tdv_logger.info("YFserciceProxy job instantiated at market open time")

    def __delete_all_market_dependant_services(self) -> None:
        self.__market_dependant_service_proxies: List[BaseServiceProxy] = []
        tdv_logger.info("YFserciceProxy job to be scheduled for deletion at market close time")

    def __schedule_daily(self, method: Callable, time: Datetime, time_zone: tzinfo) -> Job:
        return self.__scheduler.every().day.at(time.strftime('%H:%M'), time_zone).do(method)

    def __schedule_market_open_and_close_jobs(self) -> Tuple[Job, Job]:
        time_zone = self.__timezone_NY
        self.__update_today_timestamp(time_zone)
        if self.__is_market_open_today(): # If solo hacemos esto si el mercado habre hoy, no se nos bugea si lo corro el domingo?
            market_open, market_close = self.__market_times_today(self.__calendar_nyse, time_zone)
            return (self.__schedule_daily(self.__instantiate_ny_services, market_open, time_zone), # porque esto y la siguiente linea no se corren, no se ejecuta el scheduling de la 1AM.
                    self.__schedule_daily(self.__delete_all_market_dependant_services, market_close, time_zone))
        # creo que la logica de empezar el programa no está bien pensado. voy a intentar hacer un flowchart mañana

    def __is_market_open_today(self) -> bool:
        today = self.__today_ny
        valid_days: DatetimeIndex = self.__calendar_nyse.valid_days(today, today, self.__timezone_NY)
        if today.month == valid_days[0].month and today.day == valid_days[0].day:
            return True
        return False

    def __market_times_today(self, calendar: MarketCalendar, time_zone: tzinfo) -> Tuple[Datetime, Datetime]:
        schedule: DataFrame = calendar.schedule(self.__today_ny, self.__today_ny, tz=time_zone)
        return schedule['market_open'][0].to_pydatetime(), schedule['market_close'][0].to_pydatetime()

    def __update_today_timestamp(self, time_zone: timezone) -> None:
        self.__today_ny = Timestamp(Datetime.now().astimezone(time_zone))
