from typing import TYPE_CHECKING, Dict, List

from tdv.constants import TICKERS_BY_EXCHANGE
from tdv.domain.entities.exchange_entity import Exchange


if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.infra.repos.exchange_repo import ExchangeRepo
    from tdv.infra.repos.ticker_repo import TickerRepo
    from tdv.infra.repos.exchange_ticker_repo import ExchangeTickerRepo


class SetupService:
    def __init__(self, db: 'DB', exchange_repo: 'ExchangeRepo', ticker_repo: 'TickerRepo', exchange_ticker_repo: 'ExchangeTickerRepo') -> None:
        self.db = db
        self.exchange_repo = exchange_repo
        self.ticker_repo = ticker_repo
        self.exchange_ticker_repo = exchange_ticker_repo

    def create_many(self) -> Dict[str, List[str]]:
        """ Creates all exchanges and tickers """

        ticker_names_by_exchange_name = TICKERS_BY_EXCHANGE

        exchanges = [Exchange(name=name) for name in ticker_names_by_exchange_name]

        with self.db.connect as conn:
            exchanges_result = self.exchange_repo.insert(conn, exchanges)
            exchange_ids = [exchange.id for exchange in exchanges_result]

            for exchange_id in exchange_ids:
                # If ticker_name in ticker_table -> Insert in only exchange_ticker



                self.ticker_repo.select(conn, Ticker())



                # else: Insert in tickers table & exchange_ticker




                insert()

        for exchange_name, ticker_names in .values():
            for ticker_name in ticker_names:
