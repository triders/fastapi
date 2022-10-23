"""add fkey post.user_id -> users.id

Revision ID: bd82608a467b
Revises: 9c89cf2c13f0
Create Date: 2022-10-23 19:23:43.590418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd82608a467b'
down_revision = '9c89cf2c13f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(name="user_id", type_=sa.Integer, nullable=False))
    op.create_foreign_key(constraint_name="posts.user_id>users.id fkey", source_table="posts", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(constraint_name="posts.user_id>users.id fkey", table_name="posts")
    op.drop_column("posts", "user_id")
