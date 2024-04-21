"""add_exchange_table

Revision ID: f3991f66615a
Revises: 61d582bb53d3
Create Date: 2024-04-21 15:16:42.341123

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import exchange_table

# revision identifiers, used by Alembic.
revision: str = 'f3991f66615a'
down_revision: Union[str, None] = '61d582bb53d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = exchange_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
