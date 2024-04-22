"""add_insert_time_table

Revision ID: 1c9b029d0b08
Revises: 469da2b08ff7
Create Date: 2024-04-22 22:15:04.778987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c9b029d0b08'
down_revision: Union[str, None] = '469da2b08ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
