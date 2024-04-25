from typing import List, TYPE_CHECKING

from sqlalchemy import Connection

from tdv.domain.entities.company_entity import Company, CompanyLongNames, CompanyShortNames
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.company_repo import CompanyRepo


logger = LoggerFactory.make_logger(__name__)


class CompanyService:
    def __init__(self, company_repo: 'CompanyRepo') -> None:
        self.company_repo = company_repo

    def create_all_companies(self, conn: Connection) -> List[Company]:
        companies_to_insert: List[Company] = [
            Company(name=long_name, short_name=short_name)
            for long_name, short_name in zip(CompanyLongNames, CompanyShortNames)
        ]

        logger.debug('Creating all companies', companies_to_insert=companies_to_insert)

        inserted_companies = self.company_repo.insert(conn, companies_to_insert)
        return inserted_companies
