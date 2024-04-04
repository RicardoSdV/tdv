from click import group, option, Choice

from tdv.domain.entities.exchange_entity import Exchanges
from tdv.domain.entities.ticker_entity import TickersEnum
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('ticker')
def ticker_group() -> None:
    """Tickers table related operations"""


@ticker_group.command()
@option('-t', '--ticker_name', 'ticker_name', required=True, type=Choice(TickersEnum.to_list()))
@option('-e', '--exchange_name', 'exchange_name', required=True, type=Choice(Exchanges.to_list()))
def create(ticker_name: str, exchange_name: str) -> None:
    """Creates a new ticker"""

    from tdv.containers import InternalServices
    result = InternalServices.ticker_service().create_ticker(ticker_name, exchange_name)
    logger.info('Ticker created', result=result)


@ticker_group.command()
@option('-n', '--ticker_name', 'ticker_name', required=True, type=Choice(TickersEnum.to_list()))
def get(ticker_name: str) -> None:
    """Select ticker from db"""
    from tdv.containers import InternalServices
    result = InternalServices.get_ticker_by_name(ticker_name)
    logger.info('Ticker selected', result=result)
