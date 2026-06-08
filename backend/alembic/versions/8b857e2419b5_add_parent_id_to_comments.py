"""add_parent_id_to_comments

Revision ID: 8b857e2419b5
Revises: d1d4ab232c5c
Create Date: 2026-06-08 14:04:36.361792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8b857e2419b5'
down_revision: Union[str, Sequence[str], None] = 'd1d4ab232c5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('forum_comments', sa.Column('parent_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('forum_comments', 'parent_id')