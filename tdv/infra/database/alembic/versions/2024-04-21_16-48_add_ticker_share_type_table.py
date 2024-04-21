"""add_ticker_share_type_table

Revision ID: a4a567a38f5e
Revises: ef82ec3eb28a
Create Date: 2024-04-21 16:48:34.842428

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import ticker_share_type_table

# revision identifiers, used by Alembic.
revision: str = 'a4a567a38f5e'
down_revision: Union[str, None] = 'ef82ec3eb28a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


table = ticker_share_type_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)

