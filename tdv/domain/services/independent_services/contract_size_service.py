from typing import TYPE_CHECKING

from tdv.constants import CONTRACT_SIZE
from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import Connection
    from tdv.libs.log import Logger
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.infra.repos.independent_repos.contract_size_repo import ContractSizeRepo


class ContractSizeService:
    def __init__(self, entity_cache: 'EntityCache', contract_size_repo: 'ContractSizeRepo', logger: 'Logger') -> None:
        self.__entity_cache = entity_cache
        self.__contract_size_repo = contract_size_repo
        self.__logger = logger

    def create_all_contract_sizes(self, conn: 'Connection') -> 'List[ContractSize]':
        contract_sizes = [ContractSize(size=size.value, name=name) for name, size in CONTRACT_SIZE.__members__.items()]
        self.__logger.debug('Creating all ContractSizes', contract_sizes=contract_sizes)
        result = self.__contract_size_repo.insert(conn, contract_sizes)
        self.__entity_cache.cache_contract_sizes(result)
        return result

    def get_all_contract_sizes(self, conn: 'Connection') -> 'List[ContractSize]':
        contract_sizes = [ContractSize(name=name) for name in CONTRACT_SIZE.__members__]
        self.__logger.debug('Getting all ContractSizes', contract_sizes=contract_sizes)
        return self.__contract_size_repo.select(conn, contract_sizes)
