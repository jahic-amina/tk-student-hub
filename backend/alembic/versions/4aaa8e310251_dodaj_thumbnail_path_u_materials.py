"""dodaj thumbnail_path u materials
Revision ID: 4aaa8e310251
Revises: dc65c1ec3c11
Create Date: 2026-06-17 01:34:38.298557
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '4aaa8e310251'
down_revision: Union[str, Sequence[str], None] = 'dc65c1ec3c11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('materials', sa.Column('thumbnail_path', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('materials', 'thumbnail_path')
