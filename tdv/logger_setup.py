import structlog
from structlog._config import BoundLoggerLazyProxy

from tdv.common_utils import timestamp_str
from tdv.constants import LOGS_DIR_PATH


class LoggerSetup:
    def __init__(self) -> None:
        structlog.configure(
            logger_factory=structlog.WriteLoggerFactory(
                file=(LOGS_DIR_PATH / timestamp_str()).with_suffix('.log').open('w')
            ),
        )

    def get_logger(self, name: str) -> BoundLoggerLazyProxy:
        return structlog.getLogger(name)


logger_setup = LoggerSetup()
