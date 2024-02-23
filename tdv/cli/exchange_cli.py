from typing import Optional

from click import Choice, group, option

from tdv.domain.entities.exchange_entity import Exchanges
from tdv.domain.types import ExchangeId


@group('exchanges')
def exchanges_group() -> None:
    """Exchanges table related operations."""


# TODO: Add Logging
# TODO: Add help
@exchanges_group.command('create')
@option('-n', '--exchange_name', 'exchange_name', required=True, type=Choice(Exchanges.to_list()))
def create(exchange_name: str) -> None:
    from tdv.domain.internal import services
    services.exchange_service.create_exchange(exchange_name)


@exchanges_group.command('create_all')
def create_all() -> None:
    from tdv.domain.internal import services
    services.exchange_service.create_all_exchanges()


@exchanges_group.command('get')
@option('-n', '--exchange_name', 'exchange_name', required=True, default=None)
@option('-i', '--exchange_id', 'exchange_id', required=True, type=ExchangeId, default=None)
def get(exchange_name: Optional[str], exchange_id: Optional[ExchangeId]) -> None:
    from tdv.domain.internal import services

    if exchange_id:
        services.exchange_service.get_exchange_by_id(exchange_id)
    elif exchange_name:
        services.exchange_service.get_exchange_by_name(exchange_name)
    else:
        # TODO: Log no params
        pass


@exchanges_group.command('delete')
def delete() -> None:
    from tdv.domain.internal import services

