from click import Choice, group, option

from tdv.constants import ExchangeNames


@group('exchange')
def exchange_group() -> None:
    """Exchange related operations"""


@exchange_group.command('create')
@option('-n', '--exchange_name', 'exchange_name', required=True, type=Choice(ExchangeNames.to_list()))
def create(exchange_name: str) -> None:
    from tdv.domain.internal import services

    services.exchange_service.create_exchange(exchange_name)



@exchange_group.command('create_range')
def create_range() -> None:
    pass


@exchange_group.command('get_by_name')
def get_by_name() -> None:
    pass


@exchange_group.command('get_by_id')
def get_by_id() -> None:
    pass


@exchange_group.command('delete')
def delete() -> None:
    pass
