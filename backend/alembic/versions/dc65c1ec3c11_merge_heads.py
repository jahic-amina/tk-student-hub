"""merge heads

Revision ID: dc65c1ec3c11
Revises: cf1464abb805, e72918d76c2f
Create Date: 2026-06-16 17:57:16.959583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc65c1ec3c11'
down_revision: Union[str, Sequence[str], None] = ('cf1464abb805', 'e72918d76c2f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
