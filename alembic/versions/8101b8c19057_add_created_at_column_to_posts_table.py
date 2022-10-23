"""add created_at column to posts table

Revision ID: 8101b8c19057
Revises: dd300068f77a
Create Date: 2022-10-23 10:56:52.423151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8101b8c19057'
down_revision = 'dd300068f77a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(name="created_at", type_=sa.TIMESTAMP(timezone=True),
                                     server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "created_at")
