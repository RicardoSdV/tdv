from click import group, option, Choice

from tdv.domain.entities.exchange_entity import Exchanges
from tdv.domain.entities.ticker_entity import Tickers
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('tickers')
def ticker_group() -> None:
    """Tickers table related operations"""


@ticker_group.command()
@option('-t', '--ticker_name', 'ticker_name', required=True, type=Choice(Tickers.to_list()))
@option('-e', '--exchange_name', 'exchange_name', required=True, type=Choice(Exchanges.to_list()))
def create(ticker_name: str, exchange_name: str) -> None:
    """Creates a new ticker"""

    from tdv.containers import Services
    result = Services.ticker().create_ticker(ticker_name, exchange_name)
    logger.info('Ticker created', result=result)


@ticker_group.command()
def create_all() -> None:
    """Creates all tickers and exchanges in constants.TICKERS_BY_EXCHANGES"""

    from tdv.containers import Services
    from tdv.infra.database import db

    with db.connect as conn:
        exchanges = Services.exchange().create_all_exchanges(conn)
        tickers = Services.ticker().create_all_tickers(exchanges, conn)
        conn.commit()

    logger.info('Tickers & exchanges created', exchanges=exchanges, tickers=tickers)


@ticker_group.command()
@option('-n', '--ticker_name', 'ticker_name', required=True, type=Choice(Tickers.to_list()))
def get(ticker_name: str) -> None:
    """Select ticker from db"""
    from tdv.containers import Services
    result = Services.ticker().get_ticker_by_name(ticker_name)
    logger.info('Ticker selected', result=result)
