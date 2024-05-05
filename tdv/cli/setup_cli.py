from click import group

from tdv.constants import Tickers
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
        account_id = accounts[0].id
        pfol_names = []
        cashes = []
        share_counts = []
        options = []
        for name, data in local_user_portfolio_data.items():
            pfol_names.append(name)
            cashes.append(data['cash'])
            share_counts.append(data['shares'])
            options.append(data['options'])
        pfols = Service.portfolio().create_local_portfolios(account_id, pfol_names, cashes, conn)
        pfol_ids = [portfolio.id for portfolio in pfols]
        tsla_ticker_id = [ticker.id for ticker in tickers if ticker.name == Tickers.TESLA.value]
        Service.portfolio_share().create_local_portfolio_shares(pfol_ids, tsla_ticker_id[0], share_counts, conn)
        # Service.portfolio_option().create_many_portfolio_options(pfol_ids, options, conn)

        conn.commit()

    logger.info(
        'Created:',
        exchanges=exchanges,
        companies=companies,
        tickers=tickers,
        accounts=accounts,
        contract_sizes=contract_sizes,
    )
