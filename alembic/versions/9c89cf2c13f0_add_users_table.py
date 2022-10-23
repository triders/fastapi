"""add users table

Revision ID: 9c89cf2c13f0
Revises: 8101b8c19057
Create Date: 2022-10-23 11:08:00.510518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c89cf2c13f0'
down_revision = '8101b8c19057'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(name="id", type_=sa.Integer, nullable=False),
        sa.Column(name="email", type_=sa.String, nullable=False),
        sa.Column(name="password", type_=sa.String, nullable=False),
        sa.Column(name="created_at", type_=sa.TIMESTAMP(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )


def downgrade() -> None:
    op.drop_table("users")
