from typing import List, TYPE_CHECKING, Iterable, Generator

from sqlalchemy import Connection

from tdv.domain.entities.option_entities.strike_entity import Strike
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.services_internal.cache_service import CacheService
    from tdv.infra.repos.option_repos.strike_repo import StrikeRepo

logger = LoggerFactory.make_logger(__name__)


class StrikeService:
    def __init__(self, db: 'DB', strike_repo: 'StrikeRepo', cache_service: 'CacheService') -> None:
        self.__db = db
        self.__strike_repo = strike_repo
        self.__cache_service = cache_service

    def get_strikes(self, strike_ids: Generator[int, None, None], conn: Connection) -> List[Strike]:
        logger.debug('Getting strikes', strike_ids=strike_ids)
        strikes = [Strike(id=_id) for _id in strike_ids]
        result = self.__strike_repo.select(conn, strikes)
        return result

    def get_else_create_strikes(
        self, expiry_id: int, strike_prices: List[float], contract_size_names: Iterable[str], conn: Connection
    ) -> List[Strike]:

        contract_sizes = []
        for contract_size_name in contract_size_names:
            contract_size = self.__cache_service.contract_sizes_by_name.get(contract_size_name)
            if contract_size is None:
                logger.error('Unsupported contract size', contract_size_name=contract_size_name)
            contract_sizes.append(contract_size)

        logger.debug('Getting strikes', strike_prices=strike_prices)
        strikes_for_selecting = [
            Strike(expiry_id=expiry_id, contract_size_id=size.id, price=price)
            for size, price in zip(contract_sizes, strike_prices)
        ]
        selected_strikes = self.__strike_repo.select(conn, strikes_for_selecting)

        if len(selected_strikes) == len(strike_prices):
            return selected_strikes

        strikes_for_inserting = []
        for ing in strikes_for_selecting:
            for ed in selected_strikes:
                if (
                    ing.expiry_id == ed.expiry_id
                    and ing.contract_size_id == ed.contract_size_id
                    and ing.price == ed.price
                ):
                    break
            else:
                strikes_for_inserting.append(ing)

        logger.debug('Creating strikes', strikes_for_inserting=strikes_for_inserting)
        inserted_strikes = self.__strike_repo.insert(conn, strikes_for_inserting)

        return selected_strikes + inserted_strikes
