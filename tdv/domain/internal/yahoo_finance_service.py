from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from tdv.domain.entities.ticker_entity import Ticker

from tdv.domain.types import Options
from tdv.logger_setup import LoggerFactory

from tdv.utils import pretty_print

if TYPE_CHECKING:
    from tdv.infra.database import DB
    from tdv.domain.internal.cache_service import CacheService
    from tdv.domain.internal.expiry_service import ExpiryService
    from tdv.domain.internal.insert_time_service import InsertTimeService
    from tdv.domain.internal.ticker_service import TickerService

logger = LoggerFactory.make_logger(__name__)


class YahooFinanceService:
    def __init__(
        self,
        db: 'DB',
        cache_service: 'CacheService',
        ticker_service: 'TickerService',
        insert_time_service: 'InsertTimeService',
        expiry_service: 'ExpiryService',
    ) -> None:
        self.db = db
        self.__cache_service = cache_service
        self.__ticker_service = ticker_service
        self.__insert_time_service = insert_time_service
        self.__expiry_service = expiry_service

    @staticmethod
    def __str_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string, '%Y-%m-%d')


    def save_options(self, options: Options, expiry_date_strs: Iterable[str], ticker: Ticker) -> None:

        expiry_dates = [self.__str_to_datetime(date_str) for date_str in expiry_date_strs]

        with self.db.connect as conn:

            for expiry_date, option in zip(expiry_dates, options):
                calls, puts, underlying = option

                expiry = self.__expiry_service.get_else_create_expiry(expiry_date, ticker.id, conn)

                for call in calls:

                    for (
                        strike,
                        last_trade_date,
                        last_price,
                        bid,
                        ask,
                        change,
                        volume,
                        open_interest,
                        implied_volatility,
                        contract_size_name,
                    ) in zip(
                        call['lastTradeDate'].values(),
                        call['lastPrice'].values(),
                        call['bid'].values(),
                        call['ask'].values(),
                        call['change'].values(),
                        call['volume'].values(),
                        call['openInterest'].values(),
                        call['impliedVolatility'].values(),
                        call['contractSize'].values(),
                    ):

                        contract_size = self.__cache_service.contract_sizes_by_name.get(contract_size_name)
                        if contract_size is None:
                            logger.error('Unsupported contract size', contract_size_name=contract_size_name)
                            return

                        # expiry = self.__expiry_service.

                pretty_print(underlying)

                share_price = underlying['regularMarketPrice']

            # insert_time: InsertTime = self.insert_time_service.create_insert_time(conn)
            #
            #

            #
            # self.expiry_service.get_else_create_many_expiries(expiries, ticker.id,  conn)

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

        #     def create_option_get_id(
        #         self,
        #         strike: float,
        #         underlying_price: int,
        #         is_call: bool,
        #         expiry: str,
        #         ticker_id: int,
        #         conn: Connection,
        #     ) -> int:
        #
        #         option_chains = [
        #             Option(
        #                 ticker_id=ticker_id,
        #                 strike=strike,
        #                 underlying_price=underlying_price,
        #                 is_call=is_call,
        #                 expiry=str_to_datetime(expiry),
        #             )
        #         ]
        #
        #         option_chains = self.option_repo.insert(conn, option_chains)
        #         return option_chains[0].id

        # def create_options(self, options: Dict, option_chain_id: int, conn: Connection) -> None:
        #     option_entities = []

        #     for (strike, last_trade_date, last_price, bid, ask, change, volume, open_interest, implied_volatility, size,) in zip(
        #         options['lastTradeDate'].values(),
        #         options['lastPrice'].values(),
        #         options['bid'].values(),
        #         options['ask'].values(),
        #         options['change'].values(),
        #         options['volume'].values(),
        #         options['openInterest'].values(),
        #         options['impliedVolatility'].values(),
        #         options['contractSize'].values(),
        #     ):
        #         option_entities.append(
        #             OptionHistory(
        #                 option_id=option_chain_id,
        #                 last_trade_date=last_trade_date,
        #                 last_price=last_price,
        #                 bid=bid,
        #                 ask=ask,
        #                 change=change,
        #                 volume=0 if math.isnan(volume) else int(volume),
        #                 open_interest=open_interest,
        #                 implied_volatility=implied_volatility,
        #                 size=getattr(ContractSizes, size).value,
        #             )
        #         )
        #
        #     self.options_repo.insert(conn, option_entities)
