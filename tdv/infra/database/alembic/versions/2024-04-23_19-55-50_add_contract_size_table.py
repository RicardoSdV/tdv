"""add_contract_size_table

Revision ID: 26716fdefd51
Revises: 5bbb824b4af5
Create Date: 2024-04-23 19:55:50.333600

"""
from typing import Sequence, Union

from alembic import op

from tdv.infra.database.tables import contract_size_table

# revision identifiers, used by Alembic.
revision: str = '26716fdefd51'
down_revision: Union[str, None] = '5bbb824b4af5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table = contract_size_table


def upgrade() -> None:
    op.create_table(table.long_name, *[column for column in table.columns])


def downgrade() -> None:
    op.drop_table(table.long_name)
