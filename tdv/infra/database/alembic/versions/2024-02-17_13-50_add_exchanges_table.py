"""add_exchanges_table

Revision ID: 4f3e85b7cacc
Revises: 61d582bb53d3
Create Date: 2024-02-17 13:50:26.688517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.domain.entities.exchange_entity import Currencies

# revision identifiers, used by Alembic.
revision: str = '4f3e85b7cacc'
down_revision: Union[str, None] = '61d582bb53d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exchanges',
        sa.Column('id', sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(20), nullable=False, unique=True),
        sa.Column('currency', sa.String(20), server_default=Currencies.US_DOLLAR.value, nullable=False),
        sa.Column('live', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('hist', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('exchanges')
