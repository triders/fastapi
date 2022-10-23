"""add votes table

Revision ID: 1de43331c2b2
Revises: e034ca566b8c
Create Date: 2022-10-23 20:18:54.575055

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1de43331c2b2'
down_revision = 'e034ca566b8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("post_id", type_=sa.Integer, nullable=False),
        sa.Column("user_id", type_=sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(columns=("post_id",), refcolumns=("posts.id",), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(columns=("user_id",), refcolumns=("users.id",), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id")
    )


def downgrade() -> None:
    op.drop_table("votes")
