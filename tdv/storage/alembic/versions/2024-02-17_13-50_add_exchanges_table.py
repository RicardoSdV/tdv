"""add_exchanges_table

Revision ID: 4f3e85b7cacc
Revises: 61d582bb53d3
Create Date: 2024-02-17 13:50:26.688517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.constants import ExchangeNames

# revision identifiers, used by Alembic.
revision: str = '4f3e85b7cacc'
down_revision: Union[str, None] = '61d582bb53d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exchanges',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.Enum(*[item.value for item in ExchangeNames], name='exchange_names'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_exchanges_name', 'exchanges', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_exchanges_name', table_name='exchanges')
    op.drop_table('exchanges')
    op.execute('DROP TYPE IF EXISTS exchange_names;')
