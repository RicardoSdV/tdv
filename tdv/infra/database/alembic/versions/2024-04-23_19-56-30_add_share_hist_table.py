"""add_share_hist_table

Revision ID: 0665aea818f3
Revises: b6c8fc336ea3
Create Date: 2024-04-23 19:56:30.346781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import share_hist_table

# revision identifiers, used by Alembic.
revision: str = '0665aea818f3'
down_revision: Union[str, None] = 'b6c8fc336ea3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = share_hist_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
