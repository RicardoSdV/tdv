from typing import TYPE_CHECKING

from tdv.utils import datetime_from_dashed_YMD_str

if TYPE_CHECKING:
    from typing import *
    from tdv.infra.database import DB
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.domain.entities.independent_entities.contract_size_entity import ContractSize
    from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
    from tdv.domain.services.independent_services.insert_time_service import InsertTimeService
    from tdv.domain.services.option_services.expiry_service import ExpiryService
    from tdv.domain.services.option_services.strike_service import StrikeService
    from tdv.domain.services.ticker_services.ticker_service import TickerService
    from tdv.domain.services.option_services.option_hist_service import OptionHistService
    from tdv.domain.services.ticker_services.share_hist_service import ShareHistService
    from tdv.domain.types import Options
    from tdv.libs.log import Logger


class YahooFinanceService:
    def __init__(
        self,
        db: 'DB',
        entity_cache: 'EntityCache',

        ticker_service: 'TickerService',
        expiry_service: 'ExpiryService',
        strike_service: 'StrikeService',

        insert_time_service: 'InsertTimeService',
        share_hist_service : 'ShareHistService',
        option_hist_service: 'OptionHistService',

        logger: 'Logger',
    ) -> None:
        self.__db = db
        self.__entity_cache = entity_cache

        self.__ticker_service = ticker_service
        self.__expiry_service = expiry_service
        self.__strike_service = strike_service

        self.__insert_time_service = insert_time_service
        self.__share_hist_service  = share_hist_service
        self.__option_hist_service = option_hist_service

        self.__logger = logger

    def __get_contract_sizes_with_name(self, contract_size_names: 'Iterable[str]') -> 'Iterator[ContractSize]':
        for contract_size_name in contract_size_names:
            contract_size = self.__entity_cache.contract_sizes_by_name.get(contract_size_name)
            if contract_size is None:
                self.__logger.error('Unsupported contract size', contract_size_name=contract_size_name)
            yield contract_size

    def save_options(self, options: 'Options', expiry_date_strs: 'Iterable[str]', ticker: 'Ticker') -> None:
        to_datetime = datetime_from_dashed_YMD_str
        expiry_dates = [to_datetime(date_str) for date_str in expiry_date_strs]

        with self.__db.connect as conn:

            for expiry_date, (calls, puts, underlying) in zip(expiry_dates, options):

                strikes = self.__strike_service.get_else_create_strikes(
                    expiry         = self.__expiry_service.get_else_create_expiry(expiry_date, ticker, conn),
                    strike_prices  = calls['strike'].values(),
                    contract_sizes = self.__get_contract_sizes_with_name(calls['contractSize'].values()),
                    conn           = conn
                )

                insert_time = self.__insert_time_service.create_insert_time__utcnow(conn)

                share_hist = self.__share_hist_service.create_share_hist(
                    ticker      = ticker,
                    insert_time = insert_time,
                    price       = underlying['regularMarketPrice'],
                    conn        = conn
                )

                call_hists, put_hists = self.__option_hist_service.create_option_hists(
                    insert_time, strikes, calls, puts, conn
                )

                self.__entity_cache.last_share_hists_by_ticker_id = {}

            conn.commit()
