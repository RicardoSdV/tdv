"""add_ticker_table

Revision ID: 469da2b08ff7
Revises: f3991f66615a
Create Date: 2024-04-21 15:35:40.507495

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import ticker_table

# revision identifiers, used by Alembic.
revision: str = '469da2b08ff7'
down_revision: Union[str, None] = 'f3991f66615a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = ticker_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
