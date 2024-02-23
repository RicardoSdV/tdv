from sqlalchemy import Connection, Engine, create_engine

from tdv.constants import DbInfo


class DB:
    print_db_logs = True

    def __init__(self) -> None:
        self.__engine = self.__create_engine()

    @property
    def connect(self) -> Connection:
        return self.__engine.connect()

    @classmethod
    def __create_engine(cls) -> Engine:
        return create_engine(DbInfo.make_sqlalchemy_url(), echo=cls.print_db_logs)


db = DB()
