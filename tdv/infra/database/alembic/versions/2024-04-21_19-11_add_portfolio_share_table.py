"""add_portfolio_share_table

Revision ID: 2d5559c4b3cf
Revises: 51449f56ade0
Create Date: 2024-04-21 19:11:46.888734

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import portfolio_share_table

# revision identifiers, used by Alembic.
revision: str = '2d5559c4b3cf'
down_revision: Union[str, None] = '51449f56ade0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = portfolio_share_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)

