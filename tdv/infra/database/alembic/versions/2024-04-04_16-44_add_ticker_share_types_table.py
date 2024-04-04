"""add_ticker_share_types_table

Revision ID: 4f8a2a15eb5a
Revises: 522fadf789d9
Create Date: 2024-04-04 16:44:47.204259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f8a2a15eb5a'
down_revision: Union[str, None] = '522fadf789d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# TODO: Double check autogen


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticker_share_types',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('ticker_id', sa.BigInteger(), nullable=False),
    sa.Column('share_type', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticker_share_types')
    # ### end Alembic commands ###
