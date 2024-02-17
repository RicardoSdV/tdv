from sqlalchemy import create_engine, Engine

from tdv.constants import DbInfo


class DB:
    # Settings
    print_db_logs = True

    def __init__(self) -> None:
        self.__engine = self.__create_engine()

    @property
    def engine(self) -> Engine:
        return self.__engine

    @classmethod
    def __create_engine(cls) -> Engine:
        return create_engine(
            f'{DbInfo.RDBMS}+{DbInfo.DBAPI}://{DbInfo.USER}:{DbInfo.PASSWORD}@{DbInfo.HOST}:{DbInfo.PORT}/{DbInfo.NAME}',
            echo=cls.print_db_logs,
        )


db = DB()
