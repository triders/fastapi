"""create posts table

Revision ID: dd300068f77a
Revises: 
Create Date: 2022-10-23 10:26:08.979479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd300068f77a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column(name="id", type_=sa.Integer, primary_key=True, nullable=False),
        sa.Column(name="title", type_=sa.String, nullable=False),
        sa.Column(name="content", type_=sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name="posts")
