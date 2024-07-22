from typing import TYPE_CHECKING

from tdv.constants import COMPANY
from tdv.domain.entities.independent_entities.company_entity import Company

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import Connection
    from tdv.infra.repos.independent_repos.company_repo import CompanyRepo
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.libs.log import Logger


class CompanyService:
    def __init__(self, entity_cache: 'EntityCache', company_repo: 'CompanyRepo', logger: 'Logger') -> None:
        self.__entity_cache = entity_cache
        self.__company_repo = company_repo
        self.__logger = logger

    def create_all_companies(self, conn: 'Connection') -> 'List[Company]':
        companies = [
            Company(short_name=company_short_name.value, long_name=company_long_name.value)
            for company_short_name, company_long_name in zip(COMPANY.NAME, COMPANY.LONG_NAME)
        ]
        self.__logger.debug('Creating all companies', companies=companies)
        result = self.__company_repo.insert(conn, companies)
        self.__entity_cache.cache_companies(result)
        return result

    def get_all_companies(self, conn: 'Connection') -> 'List[Company]':
        companies = [Company(long_name=company_long_name.value) for company_long_name in COMPANY.LONG_NAME]
        self.__logger.debug('Getting all companies', companies=companies)
        return self.__company_repo.select(conn, companies)
