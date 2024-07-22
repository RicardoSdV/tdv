from sqlalchemy import Table, Column, BigInteger, String, Numeric, DateTime, func, ForeignKey, Integer, Boolean

from tdv.infra.database.tables import metadata
from tdv.infra.database.tables.independent_tables import account_table
from tdv.infra.database.tables.option_tables import strike_table
from tdv.infra.database.tables.ticker_tables import ticker_table

# fmt: off

portfolio_table = Table(
    'portfolio', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('account_id', BigInteger, ForeignKey(account_table.c.id, ondelete='CASCADE'), nullable=True),
    Column('name', String(1000), nullable=False),
    Column('cash', Numeric(precision=18, scale=2), nullable=False, server_default='0.00'),
    Column('created_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
)

portfolio_share_table = Table(
    'portfolio_share', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('portfolio_id', BigInteger, ForeignKey(portfolio_table.c.id, ondelete='CASCADE'), nullable=False),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('count', Numeric(precision=24, scale=10), nullable=False, server_default='0'),  # -ve = short
    Column('created_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
)

portfolio_option_table = Table(
    'portfolio_option', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('portfolio_id', BigInteger, ForeignKey(portfolio_table.c.id, ondelete='CASCADE'), nullable=False),
    Column('strike_id', BigInteger, ForeignKey(strike_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('is_call', Boolean, nullable=False),
    Column('count', Numeric(precision=24, scale=10), nullable=False, server_default='0.0'),  # -ve = sell to open
    Column('created_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now_stamp_maker(), nullable=False),
)
