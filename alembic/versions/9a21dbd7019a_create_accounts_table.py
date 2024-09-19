"""create accounts table

Revision ID: 9a21dbd7019a
Revises: 
Create Date: 2024-09-10 23:01:35.943619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a21dbd7019a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("accounts",
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.text('now()')),
                    )
    pass


def downgrade() -> None:
    op.drop_table("accounts")
    pass
