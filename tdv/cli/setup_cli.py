from click import group
from tdv.logger_setup import LoggerFactory

logger = LoggerFactory.make_logger(__name__)


@group('setup')
def setup_group() -> None:
    """Tickers table related operations"""


@setup_group.command()
def many() -> None:
    """Creates all tickers and exchanges in constants.TICKERS_BY_EXCHANGES"""

    from tdv.containers import Services
    from tdv.infra.database import db

    with db.connect as conn:
        exchanges = Services.exchange().create_all_exchanges(conn)
        tickers = Services.ticker().create_all_tickers(exchanges, conn)
        conn.commit()

    logger.info('Tickers & exchanges created', exchanges=exchanges, tickers=tickers)
