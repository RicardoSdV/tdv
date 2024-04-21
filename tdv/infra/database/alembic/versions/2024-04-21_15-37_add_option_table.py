"""add_option_table

Revision ID: ef82ec3eb28a
Revises: 7d2f3cb5e171
Create Date: 2024-04-21 15:37:57.956612

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import option_table

# revision identifiers, used by Alembic.
revision: str = 'ef82ec3eb28a'
down_revision: Union[str, None] = '7d2f3cb5e171'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = option_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
