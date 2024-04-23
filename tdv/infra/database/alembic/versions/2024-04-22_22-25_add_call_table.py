"""add_call_table

Revision ID: 15f91ab8f1a0
Revises: 3ee68448ec05
Create Date: 2024-04-22 22:25:09.422955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import call_hist_table

# revision identifiers, used by Alembic.
revision: str = '15f91ab8f1a0'
down_revision: Union[str, None] = '3ee68448ec05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = call_hist_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
