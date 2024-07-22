from datetime import datetime, timedelta
from os import makedirs, listdir
from os.path import isdir
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

from .logger import Logger
from ..schedule import Schedule, RepeatAlwaysJob, TaskNoArgs

if TYPE_CHECKING:
    from typing import *

    LoggerName = str
    StrStamp   = str
    Loggers = Dict[LoggerName, Logger]

    # The old-log-dir-deleter mechanism depends on the format of the returned stamp from LogDirNamer
    LogDirNamer   = Callable[[], StrStamp]  # being the same as the format that accepted by
    LogDirDeNamer = Callable[[StrStamp], datetime]  # <- this, the LogDirDeNamer

class LoggerFactory:
    def __init__(
            self,
            default_save_main: bool = True,
            default_save_sub : bool = True,
            default_print    : bool = True,

            main_log_name:  str   = '.main',
            logs_dir_path: 'Path' = Path('logs'),
            max_log_dirs :  int   = 20,
            save_period: 'timedelta' = timedelta(seconds=5),

            log_dir_namer  : 'LogDirNamer'   = lambda: datetime.utcnow().strftime(  '%Y-%m-%d-%H-%M-%S'),
            log_dir_denamer: 'LogDirDeNamer' = lambda _str: datetime.strptime(_str, '%Y-%m-%d-%H-%M-%S'),
    ) -> None:
        """
        LoggerFactory: Produces Logger instances, handles scheduling the saves, allows for default settings
        & more.

        WARNING: If saving logs to file, must call self.run_pending every so often

        Params:
            Unless overridden when calling LoggerFactory.make_logger the behaviour of the produced loggers
            will be according to the defaults:
            - default_save_main: Are Logger instances saving to master log?
            - default_save_sub : Are Logger instances saving to their respective sublog?
            - default_print    : Are Logger instances printing to terminal?

            - main_log_name: ...
            - logs_dir_path: Each run a dir with log files is produced, this dir is held in logs_dir_path
            - max_log_dirs : When the number of log dirs exceeds this the oldest will start getting deleted
            - save_period  : Logs will be saved every save_period given run_pending is called often enough

            - log_dir_namer  : Produces a timestamp str which will be the logger_name of this runs' logs dir logger_name
            - log_dir_denamer: Transforms the names of the log dirs to datetime objs to tell which is the oldest
        """

        # Settings ----------------------------------------
        self.__default_save_main = default_save_main
        self.__default_save_sub  = default_save_sub
        self.__default_print     = default_print

        self.__main_log_name = main_log_name
        self.__max_log_dirs  = max_log_dirs
        self.__save_period   = save_period

        self.__log_dir_denamer = log_dir_denamer

        this_run_log_dir_path = logs_dir_path / log_dir_namer()
        Logger.logs_dir_path  = this_run_log_dir_path
        Logger.main_log_path  = this_run_log_dir_path / f'{main_log_name}.log'

        self.__this_run_log_dir_path = this_run_log_dir_path
        # -------------------------------------------------

        self.__loggers: 'Loggers' = {}

        self.__schedule: 'Optional[Schedule]' = None
        self.__save_logs_job: 'Optional[RepeatAlwaysJob]' = None

        self.run_pending = self.__no_op

    def make_logger(
            self,
            logger_name: 'LoggerName',
            override_print    : 'Optional[bool]' = None,
            override_save_main: 'Optional[bool]' = None,
            override_save_sub : 'Optional[bool]' = None,
    ) -> 'Logger':
        """ Returns a Logger instance with the passed logger_name if exists else creates one.

        Save & print default settings are set in LoggerFactory.__init__ to be used in all Logger instances, but,
        they can be overridden for the specific instance returned by this method by the override params. """

        main_log_name = self.__main_log_name
        assert logger_name != main_log_name, "If sublog logger_name same as main its' entries will be duped"

        # What will the logger do? Default settings if not overridden, else, overridden settings
        will_print        = self.__default_print     if override_print     is None else override_print
        will_save_to_main = self.__default_save_main if override_save_main is None else override_save_main
        will_save_to_sub  = self.__default_save_sub  if override_save_sub  is None else override_save_sub
        # ---------------------------------------------------------------------------------------

        # If logger exists get it, if it doesn't instantiate it & add it to self.__loggers
        if logger_name in self.__loggers:
            logger = self.__loggers[logger_name]
        else:
            logger = Logger(logger_name)
            self.__loggers[logger_name] = logger

        # Important to set the correct entry handler now, for the operation of __is_any_logger_saving_to_main
        logger.set_entry_handler(will_print, will_save_to_main, will_save_to_sub)

        # If the schedule or job don't exist & they should exist instantiate them
        schedule, save_logs_job = self.__schedule, self.__save_logs_job
        if will_save_to_main or will_save_to_sub:
            if schedule is None:
                self.__schedule = schedule = Schedule()

            if save_logs_job is None:
                self.__save_logs_job = save_logs_job = RepeatAlwaysJob(self.__save_period, name='save_logs')
                schedule += save_logs_job

                self.__make_log_dir__delete_old()

        # If saves to main & the save to main task doesn't exist create it & add it to the save_logs job.
        # Since the precondition is will_save_to_main, schedule & job must be instantiated
        if will_save_to_main and main_log_name not in save_logs_job:
            save_logs_job += TaskNoArgs(Logger.save_main_log, name=main_log_name)

        # If no logs are saving to main remove saving to main task from job if exists there.
        if save_logs_job is not None and not self.__is_any_logger_saving_to_main:
            save_logs_job.remove_tasks(main_log_name)

        # If logger will save to sublog & task not in job add task to job
        if will_save_to_sub and logger_name not in save_logs_job:
            save_logs_job += TaskNoArgs(logger.save_log, logger_name)

        # If logger won't save to sublog & task in job remove task from job
        if not will_save_to_sub and save_logs_job is not None and logger_name in save_logs_job:
            save_logs_job.remove_tasks(logger_name)

        # If no tasks in job remove job from schedule remove ref to it & hopefully, that's all references
        if len(save_logs_job) == 0:
            schedule -= save_logs_job
            self.__save_logs_job = None

        # If no jobs in schedule remove reference to schedule & hopefully, all references
        if len(schedule) == 0:
            self.__schedule = None

        self.run_pending = self.__no_op if self.__schedule is None else self.__schedule.run_pending

        return logger

    def __make_log_dir__delete_old(self) -> None:
        """ Creates new log dir to save this runs' logs & deletes oldest if too many should
        only happen once per interpreter session"""

        this_run_dir = self.__this_run_log_dir_path
        if not this_run_dir.exists():
            makedirs(this_run_dir)

            dirs = [el for el in listdir(this_run_dir) if isdir(this_run_dir / el)]
            if len(dirs) > self.__max_log_dirs:  # Delete old if too many
                rmtree(min(dirs, key=self.__log_dir_denamer))

    @property
    def __is_any_logger_saving_to_main(self) -> bool:
        """ Does not ensure that the scheduling is correct nor schedule.run_pending is called appropriately."""
        for logger in self.__loggers.values():
            if logger.is_saving_to_main:
                return True
        return False

    @staticmethod
    def __no_op() -> None: pass
