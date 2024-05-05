from typing import TYPE_CHECKING, List

from sqlalchemy import Connection

from tdv.constants import ContractSizes
from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.independent_repos.contract_size_repo import ContractSizeRepo

logger = LoggerFactory.make_logger(__name__)


class ContractSizeService:
    def __init__(self, contract_size_repo: 'ContractSizeRepo') -> None:
        self.contract_size_repo = contract_size_repo

    def create_all_contract_sizes(self, conn: Connection) -> List[ContractSize]:
        contract_sizes = [ContractSize(size=size.value, name=name) for name, size in ContractSizes.__members__.items()]
        logger.debug('Creating all ContractSizes', contract_sizes=contract_sizes)
        result = self.contract_size_repo.insert(conn, contract_sizes)
        return result

    def get_all_contract_sizes(self, conn: Connection) -> List[ContractSize]:
        contract_sizes = [ContractSize(name=name) for name in ContractSizes.__members__]
        logger.debug('Getting all ContractSizes', contract_sizes=contract_sizes)
        result = self.contract_size_repo.select(conn, contract_sizes)
        return result
