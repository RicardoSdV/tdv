from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *

    LogFlag      = str
    Message   = str
    LogLine      = str  # Joined log which ends in \n
    Log          = List[LogLine]
    EntryHandler = Callable[..., None]
    # EntryHandler = Callable[[LogFlag, Message, **LoggingParam], None] <- Correct type, mypy no like

debug   = 'DEBUG  '
info    = 'INFO   '
warning = 'WARNING'
error   = 'ERROR  '
date    = 'DATE   '


class Logger:

    main_log: 'Log' = []  # Holds combined log entries
    main_current_ymdh = (-1, -1, -1, -1)

    # This is the default, if logger should get overridden by LoggerFactory
    logs_dir_path: Path = Path('logs')  # When overridden by LoggerFactory this should be this_run_
    main_log_path: Path = logs_dir_path / '.main.log'

    def __init__(self, logger_name: str) -> None:
        self.__sublog_path = self.logs_dir_path / f'{logger_name}.log'

        self.__log: 'Log' = []  # Holds log entries specific to this instance
        self.__current_ymdh = (-1, -1, -1, -1)

        # If set_entry_handler is not called the default is to only print, but it's set in the Factory
        self.__entry: 'EntryHandler' = self.__print_only

    def debug  (self, msg: str, **kwa: 'Any') -> None: self.__entry(debug  , msg, **kwa)

    def info   (self, msg: str, **kwa: 'Any') -> None: self.__entry(info   , msg, **kwa)

    def warning(self, msg: str, **kwa: 'Any') -> None: self.__entry(warning, msg, **kwa)

    def error  (self, msg: str, **kwa: 'Any') -> None: self.__entry(error  , msg, **kwa)

    def set_entry_handler(self, prnt: bool, mast: bool, subl: bool) -> None:
        if not prnt and not mast and not subl: self.__entry = self.__none
        if not prnt and not mast and     subl: self.__entry = self.__sublog
        if not prnt and     mast and     subl: self.__entry = self.__save_all
        if not prnt and     mast and not subl: self.__entry = self.__save_main
        if     prnt and not mast and not subl: self.__entry = self.__print_only
        if     prnt and not mast and     subl: self.__entry = self.__sub_n_prnt
        if     prnt and     mast and not subl: self.__entry = self.__main_n_prnt
        else:                                  self.__entry = self.__all

    def __all        (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != self.__current_ymdh:

            # Saving date to the sublog specifically
            self.__current_ymdh = ymdh
            new_date = (
                f'         : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
            )
            self.__log.append(new_date)

            # Saving date to the terminal if it hast been saved to it already by some other Logger instance
            if ymdh != Logger.main_current_ymdh:
                Logger.main_current_ymdh = ymdh
                Logger.main_log.append(new_date)

            print(new_date, end='')

        # Saving the log entry itself to master and sublogs and printing to terminal
        entry = (
            f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
            f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
        )

        print(entry, end='')
        self.__log.append(entry)
        Logger.main_log.append(entry)


    def __sublog     (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change to the sublog only
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != self.__current_ymdh:
            self.__current_ymdh = ymdh
            self.__log.append(
                (
                    f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                    f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
                )
            )

        # Saving the log entry itself to sublog only
        self.__log.append(
            (
                f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
                f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
            )
        )

    def __save_all   (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != self.__current_ymdh:

            # Saving date to the sublog specifically
            self.__current_ymdh = ymdh
            entry = (f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                     f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n')
            self.__log.append(entry)

            # Saving date to the terminal if it hast been saved to it already by some other Logger instance
            if ymdh != Logger.main_current_ymdh:
                Logger.main_current_ymdh = ymdh
                Logger.main_log.append(entry)

        # Saving the log entry itself to master and sublogs and printing to terminal
        entry = (
            f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
            f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
        )

        self.__log.append(entry)
        Logger.main_log.append(entry)

    def __save_main  (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change to master log only
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != Logger.main_current_ymdh:
            Logger.main_current_ymdh = ymdh
            Logger.main_log.append(
                (
                    f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                    f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
                )
            )

        # Saving the log entry itself to master only
        Logger.main_log.append(
            (
                f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
                f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
            )
        )

    def __print_only (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Printing complete date when year, month, day or hour change
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != Logger.main_current_ymdh:
            Logger.main_current_ymdh = ymdh
            print(
                (
                    f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                    f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
                )
            )

        # Printing the log entry itself
        print(
            (
                f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
                f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
            )
        )

    def __sub_n_prnt (self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change to sublog & print to terminal
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != self.__current_ymdh:
            self.__current_ymdh = ymdh
            entry = (
                    f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                    f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
                )
            self.__log.append(entry)
            print(entry, end='')

        # Saving the log entry itself to master and sublogs and printing to terminal
        entry = (
                f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
                f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
            )
        print(entry, end='')
        self.__log.append(entry)

    def __main_n_prnt(self, flag: str, message: str, **kwargs: 'Any') -> None:
        now = datetime.utcnow()

        # Saving complete date when year, month, day or hour change to master & print to terminal
        ymdh = (now.year, now.month, now.day, now.hour)
        if ymdh != Logger.main_current_ymdh:
            Logger.main_current_ymdh = ymdh

            entry = (
                    f'          : {date}: {ymdh[0]:04}-{ymdh[1]:02}-{ymdh[2]:02} '
                    f'{ymdh[3]:02}.{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}\n'
                )
            Logger.main_log.append(entry)
            print(entry, end='')

        # Saving the log entry itself to master & printing to terminal
        entry = (
                f"{now.minute:02}.{now.second:02}:{now.microsecond // 1000:03}: {flag}: {message} "
                f"{', '.join((f'{key}={val}' for key, val in kwargs.items()))}\n"
            )

        print(entry, end='')
        Logger.main_log.append(entry)

    def __none       (self, flag: str, message: str, **kwargs: 'Any') -> None: return

    def save_log(self) -> None:
        with open(self.__sublog_path, 'a') as f:
            f.writelines(self.__log)
        self.__log[:] = []

    @classmethod
    def save_main_log(cls) -> None:
        print('cls.main_log_path', cls.main_log_path)
        with open(cls.main_log_path, 'a') as f:
            f.writelines(cls.main_log)
        cls.main_log[:] = []

    @property
    def is_saving_to_main(self) -> bool:
        # Property better than attr bc it belongs to the class instead of the instance
        return self.__entry.__name__ in (
            '__all',
            '__save',
            '__main',
            '__main_n_prnt'
        )
