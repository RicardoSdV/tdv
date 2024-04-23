class ExchangeTicker:
    __slots__ = ('exchange_id', 'ticker_id')

    def __init__(self, exchange_id: int, ticker_id: int) -> None:
        self.exchange_id = exchange_id
        self.ticker_id = ticker_id
