from sqlalchemy import Connection


class OptionsService:
    def __init__(self, *args):
        pass

    def insert_option(self,
                      strike: float,
                      last_trade: str,
                      last_price: float,
                      bid: float,
                      ask: float,
                      change: float,
                      volume: int,
                      open_interest: int,
                      implied_volatility: float,
                      contract_size: str,
                      conn: Connection,
                      ) -> None:
        pass
