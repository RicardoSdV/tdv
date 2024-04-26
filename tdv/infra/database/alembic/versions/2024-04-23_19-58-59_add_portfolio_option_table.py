"""add_portfolio_option_table

Revision ID: 969259a3a599
Revises: a9ad5f274f59
Create Date: 2024-04-23 19:58:59.915953

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import portfolio_option_table

# revision identifiers, used by Alembic.
revision: str = '969259a3a599'
down_revision: Union[str, None] = 'a9ad5f274f59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = portfolio_option_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
