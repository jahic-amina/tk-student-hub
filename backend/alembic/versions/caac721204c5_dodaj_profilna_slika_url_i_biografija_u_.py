"""dodaj profilna_slika_url i biografija u users tabelu

Revision ID: caac721204c5
Revises: d1d4ab232c5c
Create Date: 2026-05-17 18:44:01.921366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'caac721204c5'
down_revision: Union[str, Sequence[str], None] = 'd1d4ab232c5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass



def downgrade() -> None:
    """Downgrade schema."""
    pass