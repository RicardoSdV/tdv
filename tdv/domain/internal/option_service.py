import math
from typing import Dict

from sqlalchemy import Connection

from tdv.domain.entities.option_entity import Option, ContractSizes
from tdv.infra.repos.options_repo import OptionsRepo


class OptionsService:
    def __init__(self, options_repo: OptionsRepo) -> None:
        self.options_repo = options_repo

    def create_options(self, options: Dict, option_chain_id: int, conn: Connection) -> None:
        option_entities = []

        for strike, last_trade_date, last_price, bid, ask, change, volume, open_interest, implied_volatility, size in zip(
                options['strike'].values(),
                options['lastTradeDate'].values(),
                options['lastPrice'].values(),
                options['bid'].values(),
                options['ask'].values(),
                options['change'].values(),
                options['volume'].values(),
                options['openInterest'].values(),
                options['impliedVolatility'].values(),
                options['contractSize'].values(),
        ):
            option_entities.append(
                Option(
                    option_chain_id=option_chain_id,
                    strike=strike,
                    last_trade_date=last_trade_date,
                    last_price=last_price,
                    bid=bid,
                    ask=ask,
                    change=change,
                    volume=0 if math.isnan(volume) else int(volume),
                    open_interest=open_interest,
                    implied_volatility=implied_volatility,
                    size=getattr(ContractSizes, size).value,
                )
            )

        self.options_repo.insert(conn, option_entities)
