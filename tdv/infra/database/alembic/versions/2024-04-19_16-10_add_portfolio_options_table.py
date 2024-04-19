"""add_portfolio_options_table

Revision ID: 8372765be226
Revises: 9fd14083020b
Create Date: 2024-04-19 16:10:39.290362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8372765be226'
down_revision: Union[str, None] = '9fd14083020b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio_options',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('portfolio_id', sa.BigInteger(), nullable=False),
    sa.Column('option_id', sa.BigInteger(), nullable=False),
    sa.Column('count', sa.Numeric(precision=24, scale=10), server_default='0.0', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['option_id'], ['options.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portfolio_options')
    # ### end Alembic commands ###
