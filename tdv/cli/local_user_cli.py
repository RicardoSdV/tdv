from click import group




@group('local')
def local_user_group() -> None:
    """Interface for the local user"""


@local_user_group.command()
def login() -> None:
    """Login and do all things that the local user may do"""

    from tdv.constants import LocalAccountInfo
    from tdv.containers import Cache, Service

    session_manager = Service.session_manager()
    cache_manager = Service.cache_manager()
    entity_cache = Cache.entity()

    cache_manager.init_entity_cache()
    session = session_manager.login(name=LocalAccountInfo.username, password=None)

    while True:
        print(session)

        command = input('Enter command: ')


