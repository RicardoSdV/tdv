from typing import TYPE_CHECKING, List

from sqlalchemy import Connection

from tdv.constants import ContractSizes
from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.infra.repos.independent_repos.contract_size_repo import ContractSizeRepo

logger = LoggerFactory.make_logger(__name__)


class ContractSizeService:
    def __init__(self, entity_cache: 'EntityCache', contract_size_repo: 'ContractSizeRepo') -> None:
        self.__entity_cache = entity_cache
        self.__contract_size_repo = contract_size_repo

    def create_all_contract_sizes(self, conn: Connection) -> List[ContractSize]:
        contract_sizes = [ContractSize(size=size.value, name=name.value) for size, name in zip(ContractSizes.Sizes, ContractSizes.Names)]
        logger.debug('Creating all ContractSizes', contract_sizes=contract_sizes)
        result = self.__contract_size_repo.insert(conn, contract_sizes)
        self.__entity_cache.cache_contract_sizes(result)
        return result

    def get_all_contract_sizes(self, conn: Connection) -> List[ContractSize]:
        contract_sizes = [ContractSize(name=name.value) for name in ContractSizes.Names]
        logger.debug('Getting all ContractSizes', contract_sizes=contract_sizes)
        result = self.__contract_size_repo.select(conn, contract_sizes)
        return result
