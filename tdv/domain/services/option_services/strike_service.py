from typing import TYPE_CHECKING

from tdv.domain.entities.option_entities.strike_entity import Strike

if TYPE_CHECKING:
    from typing import *
    from sqlalchemy import *

    from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
    from tdv.domain.entities.option_entities.expiry_entity import Expiry
    from tdv.infra.repos.option_repos.strike_repo import StrikeRepo
    from tdv.libs.log import Logger


class StrikeService:
    def __init__(self, strike_repo: 'StrikeRepo', logger: 'Logger') -> None:
        self.__strike_repo = strike_repo
        self.__logger = logger

    def get_else_create_strikes(
        self, expiry: 'Expiry', strike_prices: 'Collection[float]',
        contract_sizes: 'Iterable[ContractSize]', conn: 'Connection',
    ) -> 'List[Strike]':

        strikes_for_selecting = [
            Strike(expiry_id=expiry.id, contract_size_id=size.id, price=price)
            for size, price in zip(contract_sizes, strike_prices)
        ]

        self.__logger.debug('Getting strikes')
        selected_strikes = self.__strike_repo.select(conn, strikes_for_selecting)

        strikes_for_inserting = [
            selecting_strike
            for selecting_strike in strikes_for_selecting
            if not any(
                selecting_strike.expiry_id == selected_strike.expiry_id and
                selecting_strike.contract_size_id == selected_strike.contract_size_id and
                selecting_strike.price == selected_strike.price
                for selected_strike in selected_strikes
            )
        ]

        self.__logger.debug('Creating strikes', strikes_for_inserting=strikes_for_inserting)

        if strikes_for_inserting:
            inserted_strikes: List[Strike] = self.__strike_repo.insert(conn, strikes_for_inserting)
            selected_strikes.extend(inserted_strikes)

        return selected_strikes

    def get_strikes_with_ids(self, strike_ids: 'Iterator[int]', conn: 'Connection') -> 'List[Strike]':
        strikes = [Strike(id=_id) for _id in strike_ids]
        self.__logger.debug('Getting strikes', strikes=strikes)
        result = self.__strike_repo.select(conn, strikes)
        return result
