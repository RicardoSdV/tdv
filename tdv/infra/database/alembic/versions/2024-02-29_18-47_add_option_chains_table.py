"""add_options_chain_table

Revision ID: 2d4a28f7ecd3
Revises: 5343e5d7832f
Create Date: 2024-02-29 18:47:27.779687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2d4a28f7ecd3'
down_revision: Union[str, None] = '5343e5d7832f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'option_chains',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('size', sa.SmallInteger(), server_default='100', nullable=False),
        sa.Column('underlying_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('is_call', sa.Boolean(), nullable=False),
        sa.Column('expiry', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('option_chains')
