"""add_insert_time_table

Revision ID: 5bbb824b4af5
Revises: ac482fb18281
Create Date: 2024-04-23 19:55:30.402503

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables.independent_tables import insert_time_table

# revision identifiers, used by Alembic.
revision: str = '5bbb824b4af5'
down_revision: Union[str, None] = 'ac482fb18281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = insert_time_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
