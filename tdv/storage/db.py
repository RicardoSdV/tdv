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
        i = DbInfo.to_dict()
        return create_engine(
            f"{i['RDBMS']}+{i['DBAPI']}://{i['USER']}:{i['PASSWORD']}@{i['HOST']}:{i['PORT']}/{i['NAME']}",  # noformat
            echo=cls.print_db_logs,
        )
