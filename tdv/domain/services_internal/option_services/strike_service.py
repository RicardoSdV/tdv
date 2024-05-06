from datetime import datetime
from typing import List, TYPE_CHECKING, Generator

from sqlalchemy import Connection

from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
from tdv.domain.entities.option_entities.strike_entity import Strike
from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
from tdv.logger_setup import LoggerFactory

if TYPE_CHECKING:
    from tdv.infra.repos.option_repos.strike_repo import StrikeRepo
    from tdv.domain.services_internal.cache_service import CacheService
    from tdv.domain.services_internal.option_services.expiry_service import ExpiryService

logger = LoggerFactory.make_logger(__name__)


class StrikeService:
    def __init__(self, strike_repo: 'StrikeRepo', cache_service: 'CacheService', expiry_service: 'ExpiryService') -> None:
        self.__strike_repo = strike_repo
        self.__cache_service = cache_service
        self.__expiry_service = expiry_service

    def get_else_create_strikes(
        self, expiry_id: int, strike_prices: List[float], contract_sizes: List[ContractSize], conn: Connection
    ) -> List[Strike]:
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

    def get_strikes_with_ids(self, strike_ids: Generator[int, None, None], conn: Connection) -> List[Strike]:
        logger.debug('Getting strikes', strike_ids=strike_ids)
        strikes = [Strike(id=_id) for _id in strike_ids]
        result = self.__strike_repo.select(conn, strikes)
        return result

    def get_strike_with_portfolio_data(self, ticker: Ticker, strike_price: float, expiry_date: datetime, contract_size: ContractSize, conn: Connection) -> Strike:
        expiry = self.__expiry_service.get_expiry_with_ticker_and_date(ticker, expiry_date, conn)
        strike = Strike(expiry_id=expiry.id, contract_size_id=contract_size.id, price=strike_price)
        logger.debug('Getting strike', strike=strike)
        result = self.__strike_repo.select(conn, [strike])
        return result[0]
