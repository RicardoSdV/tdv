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
        print(session)  # TODO: Pretty print the session

        command = input('Enter command: ')  # TODO: Make some commands and print them

        # TODO: React to the command
