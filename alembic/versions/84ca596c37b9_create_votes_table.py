"""create votes table

Revision ID: 84ca596c37b9
Revises: 99146dc15259
Create Date: 2024-09-11 22:13:40.401283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84ca596c37b9'
down_revision: Union[str, None] = '99146dc15259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
