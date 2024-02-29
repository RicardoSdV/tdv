"""add_tickers_table

Revision ID: 5343e5d7832f
Revises: 4f3e85b7cacc
Create Date: 2024-02-29 17:43:20.793268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5343e5d7832f'
down_revision: Union[str, None] = '4f3e85b7cacc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tickers',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('exchange_id', sa.SmallInteger(), nullable=False),
        sa.Column('ticker', sa.String(length=20), nullable=False),
        sa.Column('company', sa.String(length=200), nullable=False),
        sa.Column('live', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('hist', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['exchange_id'], ['exchanges.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tickers')
