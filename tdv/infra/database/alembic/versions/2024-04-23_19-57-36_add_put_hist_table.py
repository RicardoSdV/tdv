"""add_put_hist_table

Revision ID: 73fcf6da478b
Revises: 1aeb69995334
Create Date: 2024-04-23 19:57:36.493015

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import put_hist_table

# revision identifiers, used by Alembic.
revision: str = '73fcf6da478b'
down_revision: Union[str, None] = '1aeb69995334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = put_hist_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
