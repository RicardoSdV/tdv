from typing import TYPE_CHECKING

from tdv.domain.entities.independent_entities.account_entity import Account

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *

    from tdv.infra.database import DB
    from tdv.infra.repos.independent_repos.account_repo import AccountRepo
    from tdv.libs.log import Logger


class AccountService:
    def __init__(self, db: 'DB', account_repo: 'AccountRepo', logger: 'Logger') -> None:
        self.__db = db
        self.__account_repo = account_repo
        self.__logger = logger

    def create_account(self, username: str, email: str, password: str) -> 'List[Account]':
        self.__logger.debug('Creating account', username=username, email=email, password=password)
        users = [Account(name=username, email=email, password=password)]

        with self.__db.connect as conn:
            users = self.__account_repo.insert(conn, users)
            conn.commit()

        return users

    def create_local_account(self, conn: 'Connection') -> 'List[Account]':
        from tdv.constants import LOCAL_USER
        accounts = [Account(name=LOCAL_USER.NAME, email=LOCAL_USER.EMAIL, password=LOCAL_USER.PASSWORD)]
        self.__logger.debug('Creating local account', account=accounts)
        result = self.__account_repo.insert(conn, accounts)
        return result

    def delete_account_by_id(self, user_id: int) -> 'List[Account]':
        self.__logger.debug('Deleting user by ID', user_id=user_id)
        users = [Account(id=user_id)]

        with self.__db.connect as conn:
            users = self.__account_repo.delete(conn, users)
            conn.commit()

        return users

    def get_account_by_email_and_password(self, email: str, password: str) -> 'List[Account]':
        self.__logger.debug('Selecting user by email and password', email=email, password=password)
        users = [Account(email=email, password=password)]

        with self.__db.connect as conn:
            result = self.__account_repo.select(conn, users)
            conn.commit()

        return result

    def get_or_raise_account_with_name(self, name: str, conn: 'Connection') -> 'Account':
        self.__logger.debug('Getting Account', name=name)
        accounts = self.__account_repo.select(conn, [Account(name=name)])
        assert len(accounts) == 1
        return accounts[0]

    def update_username(self, username: str, email: str, password: str) -> 'List[Account]':
        self.__logger.debug('Updating username', new_username=username, email=email, password=password)
        users = [Account(email=email, password=password)]
        params = {'username': username}

        with self.__db.connect as conn:
            result = self.__account_repo.update(conn, users, params)
            conn.commit()

        return result
