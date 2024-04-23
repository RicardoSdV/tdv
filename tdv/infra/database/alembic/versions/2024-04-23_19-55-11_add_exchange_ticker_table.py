"""add_exchange_ticker_table

Revision ID: 5575c3c78b59
Revises: ac482fb18281
Create Date: 2024-04-23 19:55:11.366239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import exchange_ticker_table

# revision identifiers, used by Alembic.
revision: str = '5575c3c78b59'
down_revision: Union[str, None] = 'ac482fb18281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = exchange_ticker_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
