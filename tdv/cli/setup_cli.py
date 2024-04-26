from click import group
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('setup')
def setup_group() -> None:
    """Tickers table related operations"""


@setup_group.command()
def many() -> None:
    """Creates all tickers companies, exchanges & local account"""

    from tdv.containers import Service
    from tdv.infra.database import db

    with db.connect as conn:
        exchanges = Service.exchange().create_all_exchanges(conn)
        companies = Service.company().create_all_companies(conn)
        tickers = Service.ticker().create_all_tickers(exchanges, companies, conn)

        accounts = Service.account().create_local_account(conn)

        conn.commit()

    logger.info('Created:', exchanges=exchanges, companies=companies, tickers=tickers, accounts=accounts)
