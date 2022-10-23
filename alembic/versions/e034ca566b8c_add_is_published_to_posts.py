"""add is_published to posts

Revision ID: e034ca566b8c
Revises: bd82608a467b
Create Date: 2022-10-23 19:35:20.737187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e034ca566b8c'
down_revision = 'bd82608a467b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("is_published", type_=sa.Boolean, server_default="False", nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "is_published")
