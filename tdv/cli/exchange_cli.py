from typing import Optional

from click import Choice, group, option

from tdv.domain.entities.exchange_entity import Exchanges
from tdv.domain.types import ExchangeId
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('exchanges')
def exchanges_group() -> None:
    """Exchanges table related operations."""


# TODO: Add help
@exchanges_group.command('create')  # todo: does not accept lower case exchange names
@option('-n', '--exchange_name', 'exchange_name', required=True, type=Choice(Exchanges.to_list()))
def create_exchange(exchange_name: str) -> None:
    """Creates a new exchange"""

    from tdv.containers import Services
    result = Services.exchange().create_exchange(exchange_name)
    logger.info('Finished creating exchange', result=result)


@exchanges_group.command('create-all')
def create_all_exchanges() -> None:
    from tdv.containers import Services
    result = Services.exchange().create_all_exchanges()
    logger.info('Finished creating all exchanges', result=result)


@exchanges_group.command('get')  # todo: does not accept lower case exchange names
@option('-n', '--exchange_name', 'exchange_name', type=str, default=None)
@option('-i', '--exchange_id', 'exchange_id', type=ExchangeId, default=None)
def get_exchange(exchange_name: Optional[str], exchange_id: Optional[ExchangeId]) -> None:
    from tdv.containers import Services

    if exchange_id:
        result = Services.exchange().get_exchange_by_id(exchange_id)
    elif exchange_name:
        result = Services.exchange().get_exchange_by_name(exchange_name)
    else:
        result = None
        logger.error('Must pass at least one arg to get exchange')

    logger.info('Finished getting exchange', result=result)


@exchanges_group.command('get-all')
def get_all_exchanges() -> None:
    from tdv.containers import Services
    result = Services.exchange().get_all_exchanges()
    logger.info('Finished getting all exchanges', result=result)


@exchanges_group.command('update-live')  # TODO: didn't check this works
@option('-n', '--exchange_name', 'exchange_name', type=str)
@option('-l', '--is_live', 'is_live', type=bool)
def update_exchange_live(exchange_name: str, is_live: bool) -> None:
    from tdv.containers import Services

    result = Services.exchange().update_exchange_live(exchange_name, is_live)

    logger.info('Finished updating live', result=result)


@exchanges_group.command('delete')
@option('-n', '--exchange_name', 'exchange_name', default=None)
@option('-i', '--exchange_id', 'exchange_id', type=ExchangeId, default=None)
def delete_exchange(exchange_name: Optional[str], exchange_id: Optional[ExchangeId]) -> None:
    from tdv.containers import Services

    if exchange_name:
        result = Services.exchange().delete_exchange_by_name(exchange_name)
    elif exchange_id:
        result = Services.exchange().delete_exchange_by_id(exchange_id)
    else:
        logger.info('Must pass at least one arg to get exchange')
        result = None

    logger.info('Finished deleting exchange', result=result)


@exchanges_group.command('delete-all')
def delete_all_exchanges() -> None:
    from tdv.containers import Services
    result = Services.exchange().delete_all_exchanges()
    logger.info('Finished deleting all exchanges', result=result)
