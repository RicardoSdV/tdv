"""add_option_chain_table

Revision ID: 7d2f3cb5e171
Revises: 469da2b08ff7
Create Date: 2024-04-21 15:36:49.064830

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import option_chain_table

# revision identifiers, used by Alembic.
revision: str = '7d2f3cb5e171'
down_revision: Union[str, None] = '469da2b08ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = option_chain_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
