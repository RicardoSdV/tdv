from datetime import datetime
from typing import TYPE_CHECKING, Tuple, Iterable

from tdv.domain.entities.insert_time_entity import InsertTime
from tdv.domain.entities.ticker_entity import Ticker
from tdv.domain.internal.expiry_service import ExpiryService

from tdv.domain.types import Options, Expiries

from tdv.utils import pretty_print

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.internal.insert_time_service import InsertTimeService
    from tdv.domain.internal.ticker_service import TickerService


class YahooFinanceService:
    def __init__(self, db: DB, ticker_service: TickerService, insert_time_service: InsertTimeService, expiry_service: ExpiryService) -> None:
        self.db = db
        self.ticker_service = ticker_service
        self.insert_time_service = insert_time_service
        self.expiry_service = expiry_service

    def save_options(self, options: Options, expiries: Iterable[str], ticker: Ticker) -> None:

        with self.db.connect as conn:
            insert_time: InsertTime = self.insert_time_service.create_insert_time(conn)


            self.expiry_service.get_else_create_many_expiries(expiries, conn)





        # with self.db.connect as conn:
        #     ticker_id = self.ticker_service.get_ticker_id_by_name(ticker_name, conn)
        #
        #     for expiry, option in zip(expiries, options):
        #         calls, puts, underlying = option
        #
        #         pretty_print(underlying)
        #
        #         return
        #
        #         # option_chain_id = self.option_chains_service.create_option_get_id(
        #         #     underlying['regularMarketPrice'], True, expiry, ticker_id, conn
        #         # )
        #         # self.options_service.create_options(calls, option_chain_id, conn)
        #         #
        #         # option_chain_id = self.option_chains_service.create_option_get_id(
        #         #     underlying['regularMarketPrice'], False, expiry, ticker_id, conn
        #         # )
        #         # self.options_service.create_options(puts, option_chain_id, conn)
        #         #
        #         # conn.commit()
