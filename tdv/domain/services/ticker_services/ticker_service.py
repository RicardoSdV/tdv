from typing import List, TYPE_CHECKING

from sqlalchemy import Connection

from tdv.constants import TICKERS_BY_COMPANY_EXCHANGE, TICKER
from tdv.domain.entities.independent_entities.company_entity import Company
from tdv.domain.entities.independent_entities.exchange_entity import Exchange
from tdv.domain.entities.ticker_entities.ticker_entity import Ticker
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)

if TYPE_CHECKING:
    from tdv.domain.cache.entity_cache import EntityCache
    from tdv.domain.services.independent_services.company_service import CompanyService
    from tdv.domain.services.independent_services.exchange_service import ExchangeService
    from tdv.infra.repos.ticker_repos.ticker_repo import TickerRepo


class TickerService:
    def __init__(
        self,
        entity_cache: 'EntityCache',
        ticker_repo: 'TickerRepo',
        exchange_service: 'ExchangeService',
        company_service: 'CompanyService',
    ) -> None:
        self.__entity_cache = entity_cache
        self.__ticker_repo = ticker_repo
        self.__exchange_service = exchange_service
        self.__company_service = company_service

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

        logger.debug('Creating all tickers', tickers=tickers)
        result = self.__ticker_repo.insert(conn, tickers)
        self.__entity_cache.cache_tickers(result)
        return result

    def get_all_tickers(self, conn: Connection) -> List[Ticker]:
        tickers = [Ticker(name=name.value) for name in TICKER]
        logger.debug('Getting all tickers', tickers=tickers)
        result = self.__ticker_repo.select(conn, tickers)
        return result
