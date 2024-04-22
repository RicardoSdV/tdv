"""add_put_table

Revision ID: a078b71ae08a
Revises: 15f91ab8f1a0
Create Date: 2024-04-22 22:26:43.705581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import put_table

# revision identifiers, used by Alembic.
revision: str = 'a078b71ae08a'
down_revision: Union[str, None] = '15f91ab8f1a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = put_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
