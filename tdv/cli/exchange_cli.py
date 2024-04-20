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
@exchanges_group.command()
@option('-n', '--exchange_name', 'exchange_name', required=True, type=Choice(Exchanges.to_list()))
def create(exchange_name: str) -> None:
    """Creates a new exchange"""

    from tdv.containers import Services
    result = Services.exchange().create_exchange(exchange_name)
    logger.info('Exchange created', result=result)


@exchanges_group.command()
def create_all() -> None:
    from tdv.containers import Services
    from tdv.infra.database import db

    with db.connect as conn:
        result = Services.exchange().create_all_exchanges(conn)
    logger.info('Exchanges created', result=result)


@exchanges_group.command()
@option('-n', '--exchange_name', 'exchange_name', type=str, default=None)
@option('-i', '--exchange_id', 'exchange_id', type=ExchangeId, default=None)
def get(exchange_name: Optional[str], exchange_id: Optional[ExchangeId]) -> None:
    from tdv.containers import Services

    if exchange_id:
        result = Services.exchange().get_exchange_by_id(exchange_id)
    elif exchange_name:
        result = Services.exchange().get_exchange_by_name(exchange_name)
    else:
        result = None
        logger.error('Must pass at least one arg to get exchange')

    logger.info('Exchange selected', result=result)


@exchanges_group.command()
@option('-n', '--exchange_name', 'exchange_name', type=str)
@option('-l', '--is_live', 'is_live', type=bool)
def update_live(exchange_name: str, is_live: bool) -> None:
    from tdv.containers import Services

    result = Services.exchange().update_exchange_live(exchange_name, is_live)

    logger.info('Exchange updated', result=result)


@exchanges_group.command()
@option('-n', '--exchange_name', 'exchange_name', default=None)
def delete(exchange_name: Optional[str]) -> None:
    from tdv.containers import Services

    if exchange_name:
        result = Services.exchange().delete_exchange_by_name(exchange_name)
    else:
        result = None
        logger.info('Must pass at least one arg to get exchange')

    logger.info('Exchange deleted', result=result)
