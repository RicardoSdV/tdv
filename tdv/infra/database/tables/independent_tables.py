""" Tables that hold no foreign keys """
from sqlalchemy import Table, Column, String, Integer, Boolean, DateTime, func, BigInteger

from tdv.constants import Currencies
from tdv.infra.database.tables import metadata

# fmt: off

exchange_table = Table(
    'exchange', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('abrv_name', String(20), nullable=False, unique=True),
    Column('name', String(150), nullable=False, unique=True),
    Column('currency', String(20), server_default=Currencies.US_DOLLAR.value, nullable=False),
    Column('live', Boolean, server_default='false', nullable=False),
    Column('hist', Boolean, server_default='false', nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

company_table = Table(
    'company', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('abrv_name', String(1000), nullable=False),
    Column('name', String(2000), nullable=False),
)

account_table = Table(
    'account', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('name', String(200), nullable=False, unique=True),
    Column('email', String(200), nullable=False, unique=True),
    Column('password', String(200), nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
)

insert_time_table = Table(
    'insert_time', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('time', DateTime, nullable=False),  # TODO: Ensure this is UTC by making it the server default
)

contract_size_table = Table(
    'contract_size', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('size', Integer, nullable=False),
    Column('name', String(50), nullable=False)
)
