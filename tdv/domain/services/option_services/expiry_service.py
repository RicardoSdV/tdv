from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.expiry_entity import Expiry

if TYPE_CHECKING:
    from typing import *
    from datetime import datetime
    from sqlalchemy import Connection
    from tdv.infra.repos.option_repos.expiry_repo import ExpiryRepo
    from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
    from tdv.libs.log import Logger


class ExpiryService:
    def __init__(self, expiry_repo: 'ExpiryRepo', logger: 'Logger') -> None:
        self.__expiry_repo = expiry_repo
        self.__logger = logger

    def get_else_create_expiry(self, expiry_date: 'datetime', ticker: 'Ticker', conn: 'Connection') -> 'Expiry':
        expiry = [Expiry(date=expiry_date, ticker_id=ticker.id)]

        self.__logger.debug('Getting expiry', expiry=expiry)
        selected_expiries = self.__expiry_repo.select(conn, expiry)
        if len(selected_expiries) > 0:
            return selected_expiries[0]

        self.__logger.debug('Expiry not found, creating expiry', expiry=expiry)
        created_expiries = self.__expiry_repo.insert(conn, expiry)

        return created_expiries[0]

    def get_expiries_with_id(self, expiry_ids: 'Iterator[int]', conn: 'Connection') -> 'List[Expiry]':
        self.__logger.debug('Getting expiries', expiry_ids=expiry_ids)
        expiries = [Expiry(id=_id) for _id in expiry_ids]
        return self.__expiry_repo.select(conn, expiries)
