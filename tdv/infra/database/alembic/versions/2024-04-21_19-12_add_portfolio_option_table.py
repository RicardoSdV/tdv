"""add_portfolio_option_table

Revision ID: 1a4693247ea6
Revises: 2d5559c4b3cf
Create Date: 2024-04-21 19:12:19.691514

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import portfolio_option_table

# revision identifiers, used by Alembic.
revision: str = '1a4693247ea6'
down_revision: Union[str, None] = '2d5559c4b3cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = portfolio_option_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)

