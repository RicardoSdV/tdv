"""add_account_table

Revision ID: 4261e68b2cc3
Revises: a4a567a38f5e
Create Date: 2024-04-21 19:05:27.588134

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import account_table

# revision identifiers, used by Alembic.
revision: str = '4261e68b2cc3'
down_revision: Union[str, None] = 'a4a567a38f5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = account_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)

