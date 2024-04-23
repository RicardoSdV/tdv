from typing import List, Optional

from sqlalchemy import Connection

from tdv.constants import TICKERS_BY_EXCHANGE
from tdv.domain.entities.exchange_entity import Exchange
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

    def create_all_tickers(self, exchanges: List[Exchange], conn: Connection) -> List[List[Ticker]]:
        results = []
        for exchange in exchanges:
            ticker_names = TICKERS_BY_EXCHANGE[exchange.name]

            tickers = [
                Ticker(
                    exchange_id=exchange.id, ticker_name=ticker_name, company_name=getattr(Companies, ticker_name.upper()).value
                )
                for ticker_name in ticker_names
            ]

            logger.debug(
                'Creating all tickers for exchange',
                exchange=exchange.name,
                tickers=tickers,
            )

            results.append(self.ticker_repo.insert(conn, tickers))
        return results

    def get_ticker_by_name(self, ticker_name: str, conn: Optional[Connection] = None) -> List[Ticker]:
        logger.debug('Getting ticker by name', ticker_name=ticker_name)
        tickers = [Ticker(ticker_name=ticker_name)]

        if conn is None:
            with self.db.connect as conn:
                result = self.ticker_repo.select(conn, tickers)
                conn.commit()
        else:
            result = self.ticker_repo.select(conn, tickers)

        return result

    def get_ticker_id_by_name(self, ticker_name: str, conn: Connection) -> int:
        logger.debug('Getting ticker id by name', ticker_name=ticker_name)
        tickers = [Ticker(ticker_name=ticker_name)]
        result = self.ticker_repo.select(conn, tickers)
        return result[0].id
