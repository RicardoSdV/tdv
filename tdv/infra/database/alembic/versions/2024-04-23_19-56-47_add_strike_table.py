"""add_strike_table

Revision ID: 3d3fb992aca9
Revises: 0665aea818f3
Create Date: 2024-04-23 19:56:47.606441

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import strike_table

# revision identifiers, used by Alembic.
revision: str = '3d3fb992aca9'
down_revision: Union[str, None] = '0665aea818f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = strike_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
