from functools import cached_property
from typing import List, TYPE_CHECKING, Tuple

from sqlalchemy import Connection

from tdv.domain.entities.atomic_entities.company_entity import Company, Companies

from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.company_repo import CompanyRepo


logger = LoggerFactory.make_logger(__name__)


class CompanyService:
    def __init__(self, db: 'DB', company_repo: 'CompanyRepo') -> None:
        self.db = db
        self.company_repo = company_repo

    @cached_property
    def companies(self) -> Tuple[Company, ...]:
        return tuple(self.get_all_companies())

    def create_all_companies(self, conn: Connection) -> List[Company]:
        companies = [
            Company(short_name=company_short_name.value, long_name=company_long_name.value)
            for company_short_name, company_long_name in zip(Companies.ShortNames, Companies.LongNames)
        ]
        logger.debug('Creating all companies', companies=companies)
        result = self.company_repo.insert(conn, companies)
        return result

    def get_all_companies(self) -> List[Company]:
        companies = [Company(long_name=company_long_name.value) for company_long_name in Companies.LongNames]
        logger.debug('Getting all companies', companies=companies)

        with self.db.connect as conn:
            result = self.company_repo.select(conn, companies)
        return result
