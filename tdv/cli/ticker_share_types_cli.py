from click import group, option, Choice

from tdv.domain.entities.ticker_entity import Tickers
from tdv.domain.entities.ticker_share_type_entity import ShareTypes
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('share-types')
def share_types_group() -> None:
    """ticker_share_types table related operations"""


@share_types_group.command()
@option('-t', '--ticker_name', 'ticker_name', required=True, type=Choice(Tickers.to_list()))
@option('-s', '--share_type', 'share_type', required=True, type=Choice(ShareTypes.to_list()))
def create(ticker_name: str, share_type: str) -> None:
    """Command to add a new share type to a ticker"""

    from tdv.containers import Services
    result = Services.share_type().create_ticker_share_type(ticker_name, share_type)
    logger.info('Share type created', result=result)


@share_types_group.command()
@option('-t', '--ticker_name', 'ticker_name', required=True, type=Choice(Tickers.to_list()))
@option('-s', '--share_type', 'share_type', required=True, type=Choice(ShareTypes.to_list()))
def delete(ticker_name: str, share_type: str) -> None:
    """Command to delete a share type from a ticker"""

    from tdv.containers import Services
    result = Services.share_type().delete_ticker_share_type(ticker_name, share_type)
    logger.info('Share type deleted', result=result)
