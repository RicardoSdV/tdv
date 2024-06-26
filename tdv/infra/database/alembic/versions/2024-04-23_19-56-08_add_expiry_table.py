"""add_expiry_table

Revision ID: b6c8fc336ea3
Revises: 26716fdefd51
Create Date: 2024-04-23 19:56:08.899109

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables.option_tables import expiry_table

# revision identifiers, used by Alembic.
revision: str = 'b6c8fc336ea3'
down_revision: Union[str, None] = '26716fdefd51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = expiry_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
