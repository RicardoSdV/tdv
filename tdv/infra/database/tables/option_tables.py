from typing import Tuple

from sqlalchemy import Table, Column, BigInteger, Integer, DateTime, ForeignKey, Numeric

from tdv.infra.database.tables import metadata
from tdv.infra.database.tables.independent_tables import contract_size_table, insert_time_table
from tdv.infra.database.tables.ticker_tables import ticker_table

# fmt: off

expiry_table = Table(
    'expiry', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('date', DateTime, nullable=False),
)

strike_table = Table(
    'strike', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('expiry_id', BigInteger, ForeignKey(expiry_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('contract_size_id', Integer, ForeignKey(contract_size_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('price', Numeric(precision=10, scale=2), nullable=False),
)


def option_hist_columns() -> Tuple[Column, ...]:
    return (
        Column('id', BigInteger, primary_key=True, autoincrement=True),
        Column('strike_id', BigInteger, ForeignKey(strike_table.c.id, ondelete='RESTRICT'), nullable=False),
        Column('insert_time_id', BigInteger, ForeignKey(insert_time_table.c.id, ondelete='RESTRICT'), nullable=False),
        Column('last_trade_date', DateTime, nullable=False),  # TODO: Find out if this is UTC and if not, change to UTC
        Column('last_price', Numeric(precision=10, scale=2), nullable=False),
        Column('bid', Numeric(precision=10, scale=2), nullable=False),
        Column('ask', Numeric(precision=10, scale=2), nullable=False),
        Column('change', Numeric(precision=10, scale=2), nullable=False),
        Column('volume', Integer, nullable=False),
        Column('open_interest', Integer, nullable=False),
        Column('implied_volatility', Numeric(precision=22, scale=20), nullable=False),
    )


call_hist_table = Table('call_hist', metadata, *option_hist_columns())

put_hist_table = Table('put_hist', metadata, *option_hist_columns())
