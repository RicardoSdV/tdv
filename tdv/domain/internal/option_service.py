from sqlalchemy import Connection

from tdv.domain.entities.option_entity import Option
from tdv.infra.repos.option_repo import OptionRepo
from tdv.utils import str_to_datetime


class OptionService:
    def __init__(self, option_repo: OptionRepo) -> None:
        self.option_repo = option_repo

    def create_option_get_id(
        self,
        strike: float,
        underlying_price: int,
        is_call: bool,
        expiry: str,
        ticker_id: int,
        conn: Connection,
    ) -> int:

        option_chains = [
            Option(
                ticker_id=ticker_id,
                strike=strike,
                underlying_price=underlying_price,
                is_call=is_call,
                expiry=str_to_datetime(expiry),
            )
        ]

        option_chains = self.option_repo.insert(conn, option_chains)
        return option_chains[0].id
