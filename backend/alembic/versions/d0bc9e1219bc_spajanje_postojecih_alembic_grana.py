"""spajanje postojecih alembic grana

Revision ID: d0bc9e1219bc
Revises: 799034ac1edf, 8b857e2419b5
Create Date: 2026-06-14 21:09:38.343765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0bc9e1219bc'
down_revision: Union[str, Sequence[str], None] = ('799034ac1edf', '8b857e2419b5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
