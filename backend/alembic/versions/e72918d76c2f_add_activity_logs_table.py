"""add_activity_logs_table
Revision ID: e72918d76c2f
Revises: 6a4113df5fcb
Create Date: 2026-05-25 22:55:41.511750
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'e72918d76c2f'
down_revision: Union[str, Sequence[str], None] = '6a4113df5fcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
