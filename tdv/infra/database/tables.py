from sqlalchemy import (
    MetaData,
    Table,
    Column,
    DateTime,
    func,
    SmallInteger,
    BigInteger,
    String,
    ForeignKey,
    Boolean,
    Numeric,
    Integer,
)

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
# Numeric(precision=24, scale=10) -> 10 000 000 000 000.000 000 000 1

exchange_table = Table(
    'exchange',
    metadata,
    Column('id', SmallInteger, primary_key=True, autoincrement=True),
    Column('name', String(20), nullable=False, unique=True),
    Column('currency', String(20), server_default=Currencies.US_DOLLAR.value, nullable=False),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

ticker_table = Table(
    'ticker',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('exchange_id', SmallInteger, ForeignKey(exchange_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('ticker', String(20), nullable=False),
    Column('company', String(200), nullable=False),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

insert_time_table = Table(
    'insert_time', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('time', DateTime, nullable=False),
)

share_history_table = Table(
    'share_history', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('insert_time_id', BigInteger, ForeignKey(insert_time_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('price', Numeric(precision=10, scale=2), nullable=False),
)

contract_size_table = Table(
    'contract_size', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('size', BigInteger, nullable=False),
)

expiry_table = Table(
    'expiry', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('contract_size_id', Integer, ForeignKey(contract_size_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('expiry', DateTime, nullable=False),
)

strike_table = Table(
    'strike', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('expiry_id', BigInteger, ForeignKey(expiry_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('strike', Numeric(precision=10, scale=2), nullable=False),
)

call_table = Table(
    'call', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('strike_id', BigInteger, ForeignKey(strike_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('insert_time_id', BigInteger, ForeignKey(insert_time_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('last_trade_date', DateTime, nullable=False),
    Column('last_price', Numeric(precision=10, scale=2), nullable=False),
    Column('bid', Numeric(precision=10, scale=2), nullable=False),
    Column('ask', Numeric(precision=10, scale=2), nullable=False),
    Column('change', Numeric(precision=10, scale=2), nullable=False),
    Column('volume', Integer, nullable=False),
    Column('open_interest', Integer, nullable=False),
    Column('implied_volatility', Numeric(precision=22, scale=20), nullable=False),
)

put_table = Table(
    'put', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('strike_id', BigInteger, ForeignKey(strike_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('insert_time_id', BigInteger, ForeignKey(insert_time_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('last_trade_date', DateTime, nullable=False),
    Column('last_price', Numeric(precision=10, scale=2), nullable=False),
    Column('bid', Numeric(precision=10, scale=2), nullable=False),
    Column('ask', Numeric(precision=10, scale=2), nullable=False),
    Column('change', Numeric(precision=10, scale=2), nullable=False),
    Column('volume', Integer, nullable=False),
    Column('open_interest', Integer, nullable=False),
    Column('implied_volatility', Numeric(precision=22, scale=20), nullable=False),
)

account_table = Table(
    'account',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('username', String(200), nullable=False, unique=True),
    Column('email', String(200), nullable=False, unique=True),
    Column('password', String(200), nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

portfolio_table = Table(
    'portfolio',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('user_id', BigInteger, ForeignKey(account_table.c.id, ondelete='CASCADE'), nullable=True),
    Column('cash', Numeric(precision=18, scale=2), nullable=False, server_default='0.00'),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

portfolio_share_table = Table(
    'portfolio_share',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('portfolio_id', BigInteger, ForeignKey(portfolio_table.c.id, ondelete='CASCADE'), nullable=False),
    Column('ticker_id', Integer, ForeignKey(ticker_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('count', Numeric(precision=24, scale=10), nullable=False, server_default='0'),
    # If negative: short
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

portfolio_call_table = Table(
    'portfolio_call',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('portfolio_id', BigInteger, ForeignKey(portfolio_table.c.id, ondelete='CASCADE'), nullable=False),
    Column('call_id', BigInteger, ForeignKey(call_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('count', Numeric(precision=24, scale=10), nullable=False, server_default='0.0'),
    # If negative: sell to open
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

portfolio_put_table = Table(
    'portfolio_put',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('portfolio_id', BigInteger, ForeignKey(portfolio_table.c.id, ondelete='CASCADE'), nullable=False),
    Column('put_id', BigInteger, ForeignKey(put_table.c.id, ondelete='RESTRICT'), nullable=False),
    Column('count', Numeric(precision=24, scale=10), nullable=False, server_default='0.0'),
    # If negative: sell to open
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)
