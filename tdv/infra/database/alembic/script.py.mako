"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

table =


def upgrade() -> None:
    ${upgrades if upgrades else "op.create_table(table.name, *[column for column in table.columns])"}


def downgrade() -> None:
    ${downgrades if downgrades else "op.drop_table(table.name)"}
