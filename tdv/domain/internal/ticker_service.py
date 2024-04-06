from typing import List

from tdv.domain.entities.ticker_entity import Ticker, Companies
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.infra.database import DB
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class TickerService:
    def __init__(self, db: 'DB', ticker_repo: 'TickerRepo', exchange_service: 'ExchangeService') -> None:
        self.db = db
        self.ticker_repo = ticker_repo
        self.exchange_service = exchange_service

    def create_ticker(self, ticker_name: str, exchange_name: str) -> List[Ticker]:
        logger.debug('Creating ticker', ticker_name=ticker_name)

        with self.db.connect as conn:

            exchanges = self.exchange_service.get_exchange_by_name(exchange_name, conn)
            exchange_id = exchanges[0].id

            company_name = getattr(Companies, ticker_name.upper()).value
            tickers = [Ticker(exchange_id=exchange_id, ticker_name=ticker_name, company_name=company_name)]

            result = self.ticker_repo.insert(conn, tickers)
            conn.commit()

        return result

    def get_ticker_by_name(self, ticker_name: str) -> List[Ticker]:
        logger.debug('Getting ticker by name', ticker_name=ticker_name)
        tickers = [Ticker(ticker_name=ticker_name)]

        with self.db.connect as conn:
            result = self.ticker_repo.select(conn, tickers)
            conn.commit()

        return result
