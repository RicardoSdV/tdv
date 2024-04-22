"""add_share_history_table

Revision ID: bcbcd82731d3
Revises: 1c9b029d0b08
Create Date: 2024-04-22 22:17:20.353502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import share_history_table

# revision identifiers, used by Alembic.
revision: str = 'bcbcd82731d3'
down_revision: Union[str, None] = '1c9b029d0b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = share_history_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
