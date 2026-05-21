"""rename tin to jib

Revision ID: 3c8c7e9e2f1b
Revises: d1d4ab232c5c
Create Date: 2026-05-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '3c8c7e9e2f1b'
down_revision: Union[str, Sequence[str], None] = 'd1d4ab232c5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('companies') as batch_op:
        batch_op.alter_column('tin', new_column_name='jib')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('companies') as batch_op:
        batch_op.alter_column('jib', new_column_name='tin')