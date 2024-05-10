from click import group




@group('local')
def local_user_group() -> None:
    """Interface for the local user"""


@local_user_group.command()
def login() -> None:
    """
    The local user workflow should:
        1. Login to load all the portfolio data into the Session from the DB
        2. Modify, create or delete portfolios, pfol_options etc. in the Session, i.e. no DB connections opened
        3. Logout, saving all the new changes to the DB with one connection
    """

    from tdv.domain.entities.portfolio_entities.portfolio_entity import Portfolio

    from tdv.constants import LOCAL_USER
    from tdv.containers import Cache, Service

    session_manager = Service.session_manager()
    cache_manager = Service.cache_manager()
    entity_cache = Cache.entity()
    pfol_service = Service.portfolio()

    cache_manager.init_entity_cache()
    session = session_manager.login(name=LOCAL_USER.NAME, password=None)
    account = session.account

    while True:

        print(session)  # TODO: Define an appropriate def __repr__(): in the session which pretty prints its data

        print('1: Create portfolio')
        print('2: Logout')
        print()
        command = input('Enter command: ')
        if command == '1':
            name = input('  Portfolio name: ')
            cash = int(input('  Cash: '))

            portfolio = Portfolio(account_id=account.id, name=name, cash=cash)
            session.portfolios_by_name[name] = portfolio

            print(' Created: ', portfolio)

        elif command == '2':
            session_manager.logout(account.name)


