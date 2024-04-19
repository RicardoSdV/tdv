"""add_options_table

Revision ID: c58c508cb17d
Revises: 2d4a28f7ecd3
Create Date: 2024-02-29 19:04:17.768524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c58c508cb17d'
down_revision: Union[str, None] = '2d4a28f7ecd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'options',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('option_chain_id', sa.BigInteger(), nullable=False),
        sa.Column('strike', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('last_trade', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('last_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('bid', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('ask', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('change', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('volume', sa.Integer(), nullable=False),
        sa.Column('open_interest', sa.Integer(), nullable=False),
        sa.Column('implied_volatility', sa.Integer(), nullable=False),
        sa.Column('size', sa.Integer(), server_default='100', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['option_chain_id'], ['option_chains.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('options')
