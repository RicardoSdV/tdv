"""add_expiry_table

Revision ID: 892241b2816c
Revises: c03db9b5a7cf
Create Date: 2024-04-22 22:23:17.526748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import expiry_table

# revision identifiers, used by Alembic.
revision: str = '892241b2816c'
down_revision: Union[str, None] = 'c03db9b5a7cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = expiry_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
