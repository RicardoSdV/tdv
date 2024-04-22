"""add_strike_table

Revision ID: 3ee68448ec05
Revises: 892241b2816c
Create Date: 2024-04-22 22:24:02.136075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import strike_table

# revision identifiers, used by Alembic.
revision: str = '3ee68448ec05'
down_revision: Union[str, None] = '892241b2816c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = strike_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
