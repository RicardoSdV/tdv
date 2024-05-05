from functools import cached_property
from typing import List, TYPE_CHECKING, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.company_entity import Company, Companies

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.company_repo import CompanyRepo


logger = LoggerFactory.make_logger(__name__)


class CompanyService:
    def __init__(self, db: 'DB', company_repo: 'CompanyRepo') -> None:
        self.db = db
        self.company_repo = company_repo

    def create_all_companies(self, conn: Connection) -> List[Company]:
        companies = [
            Company(abrv_name=abrv_name.value, name=name.value)
            for abrv_name, name in zip(Companies.AbrvNames, Companies.Names)
        ]
        logger.debug('Creating all companies', companies=companies)
        result = self.company_repo.insert(conn, companies)
        return result

    def get_all_companies(self, conn: Connection) -> List[Company]:
        companies = [Company(abrv_name=abrv_name.value) for abrv_name in Companies.Names]
        logger.debug('Getting all companies', companies=companies)
        result = self.company_repo.select(conn, companies)
        return result
