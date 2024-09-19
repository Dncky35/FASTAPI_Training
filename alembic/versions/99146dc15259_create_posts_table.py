"""create posts table

Revision ID: 99146dc15259
Revises: 9a21dbd7019a
Create Date: 2024-09-11 21:38:23.302985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99146dc15259'
down_revision: Union[str, None] = '9a21dbd7019a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column("title", sa.String, nullable=False),
                    sa.Column("content", sa.String, nullable=False),
                    sa.Column("published", sa.BOOLEAN, server_default='True', nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('Now()'), nullable=False),
                    # FOR FOREIGN KEY
                    sa.Column("account_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key("posts_accounts_fk", source_table="posts", referent_table="accounts", local_cols=["account_id"], remote_cols=["id"], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
