"""add_company_table

Revision ID: 936afec1a05a
Revises: bc5cb1f3e078
Create Date: 2024-04-23 19:53:24.652089

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import company_table

# revision identifiers, used by Alembic.
revision: str = '936afec1a05a'
down_revision: Union[str, None] = 'bc5cb1f3e078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = company_table


def upgrade() -> None:
    op.create_table(table.long_name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.long_name)
