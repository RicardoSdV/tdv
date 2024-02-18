from sqlalchemy import MetaData, Table, Column, DateTime, func, Index, Enum, SmallInteger

from tdv.constants import ExchangeNames

metadata = MetaData()

exchanges_table = Table(
    'exchanges', metadata,
    Column('id', SmallInteger, primary_key=True, autoincrement=True),
    Column('name', Enum(*[item.value for item in ExchangeNames]), nullable=False),
    Column('created_at', DateTime, server_default=func.now(), nullable=False),
    Column('updated_at', DateTime, server_default=func.now(), nullable=False),
    Index('ix_exchanges_name', 'name', unique=True),
)
