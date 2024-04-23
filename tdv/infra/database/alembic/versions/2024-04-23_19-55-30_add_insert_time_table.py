"""add_insert_time_table

Revision ID: 5bbb824b4af5
Revises: 5575c3c78b59
Create Date: 2024-04-23 19:55:30.402503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import insert_time_table

# revision identifiers, used by Alembic.
revision: str = '5bbb824b4af5'
down_revision: Union[str, None] = '5575c3c78b59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = insert_time_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)