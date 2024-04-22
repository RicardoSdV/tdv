from tdv.domain.internal.option_service import OptionService
from tdv.domain.internal.option_history_service import OptionHistoryService
from tdv.domain.internal.ticker_service import TickerService
from tdv.domain.types import Options, Expiries
from tdv.infra.database import DB
from tdv.utils import pretty_print


class YahooFinanceService:
    def __init__(
        self,
        db: DB,
        ticker_service: TickerService,
        option_chains_service: OptionService,
        options_service: OptionHistoryService,
    ) -> None:
        self.db = db
        self.ticker_service = ticker_service
        self.option_chains_service = option_chains_service
        self.options_service = options_service

    def save_option(self, options: Options, expiries: Expiries, ticker_name: str) -> None:
        with self.db.connect as conn:
            ticker_id = self.ticker_service.get_ticker_id_by_name(ticker_name, conn)

            for expiry, option in zip(expiries, options):
                calls, puts, underlying = option

                pretty_print(underlying)

                return

                option_chain_id = self.option_chains_service.create_option_get_id(
                    underlying['regularMarketPrice'], True, expiry, ticker_id, conn
                )
                self.options_service.create_options(calls, option_chain_id, conn)

                option_chain_id = self.option_chains_service.create_option_get_id(
                    underlying['regularMarketPrice'], False, expiry, ticker_id, conn
                )
                self.options_service.create_options(puts, option_chain_id, conn)

                conn.commit()
