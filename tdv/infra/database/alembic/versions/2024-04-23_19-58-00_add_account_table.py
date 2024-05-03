"""add_account_table

Revision ID: 5706223ab0bd
Revises: 73fcf6da478b
Create Date: 2024-04-23 19:58:00.786824

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import account_table

# revision identifiers, used by Alembic.
revision: str = '5706223ab0bd'
down_revision: Union[str, None] = '73fcf6da478b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = account_table


def upgrade() -> None:
    op.create_table(table.long_name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.long_name)
