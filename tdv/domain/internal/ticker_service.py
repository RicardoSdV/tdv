from typing import List, Optional, Tuple

from sqlalchemy import Connection

from tdv.constants import TICKERS_BY_COMPANY_EXCHANGE
from tdv.domain.entities.company_entity import Company
from tdv.domain.entities.exchange_entity import Exchange
from tdv.domain.entities.ticker_entity import Ticker, Tickers
from tdv.domain.internal.company_service import CompanyService
from tdv.domain.internal.exchange_service import ExchangeService
from tdv.infra.database import DB
from tdv.infra.repos.ticker_repo import TickerRepo
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


class TickerService:
    def __init__(
        self,
        db: 'DB',
        ticker_repo: 'TickerRepo',
        exchange_service: 'ExchangeService',
        company_service: 'CompanyService',
    ) -> None:
        self.db = db
        self.ticker_repo = ticker_repo
        self.exchange_service = exchange_service
        self.company_service = company_service

    def create_all_tickers(self, exchanges: List[Exchange], companies: List[Company], conn: Connection) -> List[Ticker]:
        tickers = []
        for exchange_name, company_ticker_names in TICKERS_BY_COMPANY_EXCHANGE.items():
            exchange_id = None
            for exchange in exchanges:
                if exchange.name == exchange_name.value:
                    exchange_id = exchange.id
                    break
            if exchange_id is None:
                continue

            for company_name, ticker_names in company_ticker_names.items():
                company_id = None
                for company in companies:
                    if company.long_name == company_name.value:
                        company_id = company.id
                        break
                if company_id is None:
                    continue

                for ticker_name in ticker_names:
                    tickers.append(Ticker(exchange_id=exchange_id, company_id=company_id, name=ticker_name.value))

        logger.debug('Inserting tickers', tickers=tickers)
        result = self.ticker_repo.insert(conn, tickers)
        return result

    def get_all_tickers(self, conn: Connection) -> List[Ticker]:
        tickers = [Ticker(name=name.value) for name in Tickers]
        logger.debug('Getting all tickers', tickers=tickers)
        result = self.ticker_repo.insert(conn, tickers)
        return result

    def get_ticker_by_name(self, ticker_name: str, conn: Optional[Connection] = None) -> List[Ticker]:
        logger.debug('Getting ticker by name', ticker_name=ticker_name)
        tickers = [Ticker(name=ticker_name)]

        if conn is None:
            with self.db.connect as conn:
                result = self.ticker_repo.select(conn, tickers)
                conn.commit()
        else:
            result = self.ticker_repo.select(conn, tickers)

        return result

    def get_ticker_id_by_name(self, ticker_name: str) -> Optional[int]:
        for ticker in self.tickers:
            if ticker.long_name == ticker_name:
                return ticker.id
        return None
