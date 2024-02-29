from sqlalchemy import MetaData, Table, Column, DateTime, func, Index, SmallInteger, BigInteger, String, ForeignKey, \
    Boolean, Numeric, Integer

from tdv.domain.entities.exchange_entity import Currencies

"""
All SQL Alchemy Tables are defined here.

ATTENTION: Many columns that are represented as Enums in the code will not be in the DB due to the complexities
of keeping Enums updated correctly. Therefore, all validation for these types happens when assigning these values to
Entity descendant attributes, so, it's not recommended to bypass this step when inserting into a table with an Enum
"""

metadata = MetaData()

# SmallInteger -> +- 32 000  (2 bytes)
# Integer -> +- 2 000 000 000  (4 bytes)
# BigInteger ->  +- 9 000 000 000 000 000 000  (8 bytes)
# Numeric(precision=10, scale=2) -> 10 000 000.01

exchanges_table = Table(
    'exchanges', metadata,
    Column('id', SmallInteger, primary_key=True, autoincrement=True),
    Column('name', String(20), nullable=False),
    Column('currency', String(20), server_default=Currencies.US_DOLLAR.value, nullable=False),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

tickers_table = Table(
    'tickers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('exchange_id', SmallInteger, ForeignKey(exchanges_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('ticker', String(20), nullable=False),
    Column('company', String(200), nullable=False),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

option_chains_table = Table(
    'option_chains', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('ticker_id', Integer, ForeignKey(tickers_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('size', SmallInteger, server_default='100', nullable=False),
    Column('underlying_price', Numeric(precision=10, scale=2), nullable=False),
    Column('is_call', Boolean, nullable=False),
    Column('expiry', DateTime, nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

options_table = Table(
    'options', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('option_chain_id', BigInteger, ForeignKey(option_chains_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('strike', Numeric(precision=10, scale=2), nullable=False),
    Column('last_trade', Numeric(precision=10, scale=2), nullable=False),
    Column('last_price', Numeric(precision=10, scale=2), nullable=False),
    Column('bid', Numeric(precision=10, scale=2), nullable=False),
    Column('ask', Numeric(precision=10, scale=2), nullable=False),
    Column('change', Numeric(precision=10, scale=2), nullable=False),
    Column('volume', Integer, nullable=False),
    Column('open_interest', Integer, nullable=False),
    Column('implied_volatility', Integer, nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
)
