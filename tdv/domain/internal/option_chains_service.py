from sqlalchemy import Connection

from tdv.domain.entities.option_chain_entity import OptionChain
from tdv.domain.internal.ticker_service import TickerService
from tdv.infra.repos.option_chains_repo import OptionChainsRepo
from tdv.utils import str_to_datetime


class OptionChainsService:

    def __init__(self, option_chains_repo: OptionChainsRepo, ticker_service: TickerService) -> None:
        self.option_chains_repo = option_chains_repo
        self.ticker_service = ticker_service

    def create_option_chain_get_id(
            self, underlying_price: int, is_call: bool, expiry: str, ticker_name: str, conn: Connection
    ) -> int:

        ticker_id = self.ticker_service.get_ticker_id_by_name(ticker_name, conn)
        option_chains = [OptionChain(
            ticker_id=ticker_id, underlying_price=underlying_price, is_call=is_call, expiry=str_to_datetime(expiry)
        )]

        option_chains = self.option_chains_repo.insert(conn, option_chains)
        return option_chains[0].id
