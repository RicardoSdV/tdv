from tdv.domain.internal.option_chains_service import OptionChainsService
from tdv.domain.internal.option_service import OptionsService
from tdv.domain.types import OptionChains, Expiries
from tdv.infra.database import DB
from tdv.utils import pretty_print


class YahooFinanceService:

    def __init__(self, db: DB, option_chains_service: OptionChainsService, options_service: OptionsService) -> None:
        self.db = db
        self.option_chains_service = option_chains_service
        self.options_service = options_service

    def save_option_chains(self, option_chains: OptionChains, expiries: Expiries, ticker_name: str) -> None:

        for expiry, option_chain in zip(expiries, option_chains):
            calls, puts, underlying = option_chain

            # pretty_print(puts)
            # return

            with self.db.connect as conn:

                option_chain_id = self.option_chains_service.create_option_chain_get_id(
                    underlying['regularMarketPrice'], True, expiry, ticker_name, conn
                )
                self.options_service.create_options(calls, option_chain_id, conn)

                # option_chain_id = self.option_chains_service.create_option_chain_get_id(
                #     underlying['regularMarketPrice'], False, expiry, ticker_name, conn
                # )
                # self.options_service.create_options(puts, option_chain_id, conn)

                conn.commit()
