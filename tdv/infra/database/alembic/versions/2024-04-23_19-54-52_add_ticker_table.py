"""add_ticker_table

Revision ID: ac482fb18281
Revises: 20ba9df6a3ca
Create Date: 2024-04-23 19:54:52.638568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import ticker_table

# revision identifiers, used by Alembic.
revision: str = 'ac482fb18281'
down_revision: Union[str, None] = '20ba9df6a3ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = ticker_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
