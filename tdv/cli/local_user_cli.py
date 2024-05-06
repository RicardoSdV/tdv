from click import group


@group('local')
def local_user_group() -> None:
    """Interface for the local user"""


@local_user_group.command()
def login() -> None:
    """Login and do all things that the local user may do"""

    from tdv.containers import Service

    session_manager = Service.session_manager()
    session = session_manager.login()

    while True:
        print(session)



        command = input('Enter command: ')


