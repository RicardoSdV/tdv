"""
All sql alchemy tables defined in this module

ATTENTION: Use enums and entities for validation instead of holding enums in DB

ATTENTION: Make sure all times are in UTC

"""

from sqlalchemy import MetaData

metadata = MetaData()
