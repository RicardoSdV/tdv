"""add_contract_size_table

Revision ID: c03db9b5a7cf
Revises: bcbcd82731d3
Create Date: 2024-04-22 22:22:09.606133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tdv.infra.database.tables import contract_size_table

# revision identifiers, used by Alembic.
revision: str = 'c03db9b5a7cf'
down_revision: Union[str, None] = 'bcbcd82731d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = contract_size_table


def upgrade() -> None:
    op.create_table(table.name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.name)
