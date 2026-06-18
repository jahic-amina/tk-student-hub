"""extend forum notifications

Revision ID: 9e329cbb238c
Revises: 6b10b374a39c
Create Date: 2026-06-18 14:40:06.094240
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9e329cbb238c"
down_revision: Union[str, Sequence[str], None] = "6b10b374a39c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = [column["name"] for column in inspector.get_columns("forum_notifications")]
    indexes = [index["name"] for index in inspector.get_indexes("forum_notifications")]

    if "comment_id" not in columns:
        op.add_column(
            "forum_notifications",
            sa.Column("comment_id", sa.Integer(), nullable=True),
        )

    if "is_hidden" not in columns:
        op.add_column(
            "forum_notifications",
            sa.Column(
                "is_hidden",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("0"),
            ),
        )

    if "ix_forum_notifications_comment_id" not in indexes:
        op.create_index(
            "ix_forum_notifications_comment_id",
            "forum_notifications",
            ["comment_id"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = [column["name"] for column in inspector.get_columns("forum_notifications")]
    indexes = [index["name"] for index in inspector.get_indexes("forum_notifications")]

    if "ix_forum_notifications_comment_id" in indexes:
        op.drop_index(
            "ix_forum_notifications_comment_id",
            table_name="forum_notifications",
        )

    if "is_hidden" in columns:
        op.drop_column("forum_notifications", "is_hidden")

    if "comment_id" in columns:
        op.drop_column("forum_notifications", "comment_id")