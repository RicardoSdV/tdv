"""add_exchange_table

Revision ID: 20ba9df6a3ca
Revises: 936afec1a05a
Create Date: 2024-04-23 19:54:34.519096

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import exchange_table

# revision identifiers, used by Alembic.
revision: str = '20ba9df6a3ca'
down_revision: Union[str, None] = '936afec1a05a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = exchange_table


def upgrade() -> None:
    op.create_table(table.long_name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.long_name)
