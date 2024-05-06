from click import group

from local_user_data.portfolio_data import local_user_portfolio_data
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
        local_account = Service.account().create_local_account(conn)[0]
        pfol_combo = Service.portfolio().create_all_local_user_portfolios(local_account, conn)
        portfolios, portfolio_shares, portfolio_options = pfol_combo

        conn.commit()

    logger.info(
        'Created:',
        exchanges=exchanges,
        companies=companies,
        tickers=tickers,
        accounts=local_account,
        contract_sizes=contract_sizes,
        portfolios=portfolios,
        portfolio_shares=portfolio_shares,
        portfolio_options=portfolio_options,
    )
