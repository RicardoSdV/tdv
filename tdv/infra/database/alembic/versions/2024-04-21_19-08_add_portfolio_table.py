"""add_portfolio_table

Revision ID: 51449f56ade0
Revises: 4261e68b2cc3
Create Date: 2024-04-21 19:08:29.399736

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import portfolio_table

# revision identifiers, used by Alembic.
revision: str = '51449f56ade0'
down_revision: Union[str, None] = '4261e68b2cc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = portfolio_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
