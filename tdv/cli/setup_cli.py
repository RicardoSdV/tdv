from click import group

from tdv.domain.testing.test_data.portfolio_data import local_user_portfolio_data
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('setup')
def setup_group() -> None:
    """Tickers table related operations"""


@setup_group.command()
def many() -> None:
    """Creates all tickers companies, exchanges & local account with portfolios"""

    from tdv.containers import Service
    from tdv.infra.database import db

    with db.connect as conn:
        exchanges = Service.exchange().create_all_exchanges(conn)
        companies = Service.company().create_all_companies(conn)
        tickers = Service.ticker().create_all_tickers(exchanges, companies, conn)
        contract_sizes = Service.contract_size().create_all_contract_sizes(conn)
        accounts = Service.account().create_local_account(conn)

    logger.info(
        'Created:',
        exchanges=exchanges,
        companies=companies,
        tickers=tickers,
        accounts=accounts,
        contract_sizes=contract_sizes,
    )


def portfolios():

    from tdv.containers import Service
    from tdv.infra.database import db

    account_id = 1
    ticker_id = 1

    with db.connect as conn:
        # portfolio
        names = []
        cashes = []
        counts = []
        options = []
        for name, data in local_user_portfolio_data.items():
            names.append(name)
            cashes.append(data['cash'])
            counts.append(data['shares'])
            options.append(data['options'])
        portfolios = Service.portfolio().create_many_portfolios(account_id, names, cashes, conn)

        # portfolio shares
        portfolio_ids = [portfolio.id for portfolio in portfolios]
        Service.portfolio_share().create_many_portfolio_shares(portfolio_ids, ticker_id, counts, conn)

        # portfolio options
        Service.portfolio_option().create_many_portfolio_options(portfolio_ids, options, conn)

        conn.commit()
