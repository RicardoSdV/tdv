""" Ticker related tables """
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, func, ForeignKey, BigInteger, Numeric

from tdv.infra.database.tables import metadata
from tdv.infra.database.tables.independent_tables import exchange_table, company_table, insert_time_table

# fmt: off

ticker_table = Table(
    'ticker', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('exchange_id', Integer, ForeignKey(exchange_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('company_id', Integer, ForeignKey(company_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('name', String(50), nullable=False, unique=True),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

share_hist_table = Table(
    'share_hist', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('insert_time_id', BigInteger, ForeignKey(insert_time_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('price', Numeric(precision=10, scale=2), nullable=False),
)
