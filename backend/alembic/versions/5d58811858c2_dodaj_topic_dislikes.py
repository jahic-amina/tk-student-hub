"""dodaj topic dislikes

Revision ID: 5d58811858c2
Revises: 9e329cbb238c
Create Date: 2026-06-18 16:43:16.793528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d58811858c2'
down_revision: Union[str, Sequence[str], None] = '9e329cbb238c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'topic_dislikes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['topic_id'], ['forum_topics.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('topic_id', 'user_id', name='unique_topic_dislike_per_user')
    )

    op.create_index(
        op.f('ix_topic_dislikes_topic_id'),
        'topic_dislikes',
        ['topic_id'],
        unique=False
    )

    op.create_index(
        op.f('ix_topic_dislikes_user_id'),
        'topic_dislikes',
        ['user_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_topic_dislikes_user_id'), table_name='topic_dislikes')
    op.drop_index(op.f('ix_topic_dislikes_topic_id'), table_name='topic_dislikes')
    op.drop_table('topic_dislikes')
