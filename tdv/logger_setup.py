import structlog
from structlog._config import BoundLoggerLazyProxy

from tdv.utils import dashed_str_YMDHMS_utcnow
from tdv.constants import PATH


class LoggerFactory:
    __save_to_file = False
    if __save_to_file:
        structlog.configure(
            logger_factory=structlog.WriteLoggerFactory(
                file=(PATH.DIR.LOGS / dashed_str_YMDHMS_utcnow()).with_suffix('.log').open('w')
            ),
        )

    @staticmethod
    def make_logger(name: str) -> BoundLoggerLazyProxy:
        return structlog.getLogger(name)


# Experimental logger
# import importlib
#
# import structlog
#
# from tdv.common_utils import timestamp_str
# from tdv.constants import LOGS_DIR_PATH
#
# # write_log = importlib.reload(structlog)
#
#
# class Logger:
#     __print_logs = True
#     __write_logs = True
#     #
#     # test_log = structlog.get_logger(__name__)
#     # test_log.info('logger init', myarg='test')
#
#     if __write_logs:
#         structlog.configure(logger_factory=structlog.WriteLoggerFactory(
#             file=(LOGS_DIR_PATH / timestamp_str()).with_suffix('.log').open('w'))
#         )
#
#     def __init__(self, name: str = '') -> None:
#         # write_log.get_logger(name),
#         # self.__loggers = [structlog.get_logger(name)]
#         self.__loggers = [structlog.get_logger(name)]
#
#         # self.__write_logger = write_log.get_logger(name)
#         # self.__print_logger = print_log.get_logger(name)
#
#     def info(self, *args, **kwargs) -> None:
#         for logger in self.__loggers:
#             logger.info(*args, **kwargs)
#
#     def debug(self, *args, **kwargs) -> None:
#         for logger in self.__loggers:
#             logger.debug(*args, **kwargs)
#
#     def warning(self, *args, **kwargs) -> None:
#         for logger in self.__loggers:
#             logger.warning(*args, **kwargs)
#
#     def error(self, *args, **kwargs) -> None:
#         for logger in self.__loggers:
#             logger.error(*args, **kwargs)
#
#     def critical(self, *args, **kwargs) -> None:
#         for logger in self.__loggers:
#             logger.critical(*args, **kwargs)
