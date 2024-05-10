from sqlalchemy import Connection, Engine, create_engine

from tdv.constants import DB_INFO


class DB:
    print_db_logs = False

    def __init__(self) -> None:
        self.__engine = self.__create_engine()

    @property
    def connect(self) -> Connection:
        return self.__engine.connect()

    @classmethod
    def __create_engine(cls) -> Engine:
        return create_engine(DB_INFO.URL, echo=cls.print_db_logs)


db = DB()
