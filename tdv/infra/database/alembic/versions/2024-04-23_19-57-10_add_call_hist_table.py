"""add_call_hist_table

Revision ID: 1aeb69995334
Revises: 3d3fb992aca9
Create Date: 2024-04-23 19:57:10.443757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import call_hist_table

# revision identifiers, used by Alembic.
revision: str = '1aeb69995334'
down_revision: Union[str, None] = '3d3fb992aca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = call_hist_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
