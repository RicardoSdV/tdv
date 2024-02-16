"""init

Revision ID: 69a5d59efbc4
Revises: 
Create Date: 2024-02-14 20:46:30.610953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.constants import Exchanges

# revision identifiers, used by Alembic.
revision: str = '69a5d59efbc4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exchanges',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.Enum(*[item.value for item in Exchanges], name='exchange_names'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_exchanges_name', 'exchanges', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_exchanges_name', table_name='exchanges')
    op.drop_table('exchanges')
    op.execute('DROP TYPE IF EXISTS exchange_names;')
