"""add_portfolio_share_table

Revision ID: a9ad5f274f59
Revises: a7af800b4e24
Create Date: 2024-04-23 19:58:42.103214

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables.portfolio_tables import portfolio_share_table

# revision identifiers, used by Alembic.
revision: str = 'a9ad5f274f59'
down_revision: Union[str, None] = 'a7af800b4e24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = portfolio_share_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
