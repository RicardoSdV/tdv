"""add_portfolio_table

Revision ID: a7af800b4e24
Revises: 5706223ab0bd
Create Date: 2024-04-23 19:58:20.100828

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import portfolio_table

# revision identifiers, used by Alembic.
revision: str = 'a7af800b4e24'
down_revision: Union[str, None] = '5706223ab0bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = portfolio_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
