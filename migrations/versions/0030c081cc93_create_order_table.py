"""create orders table

Revision ID: 0030c081cc93
Revises: 0
Create Date: 2024-03-08 17:12:43.291938

"""
from alembic import op
from sqlalchemy import String, Column, DateTime, Integer, func

# revision identifiers, used by Alembic.
revision = "0030c081cc93"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "orders",
        Column("id", Integer, primary_key=True),
        Column("name", String(300), nullable=False),
        Column("address", String(300), nullable=False),
        Column("created_at", DateTime, nullable=False, server_default=func.now()),
        Column("updated_at", DateTime, nullable=False, server_default=func.now(),
               onupdate=func.now()),
    )


def downgrade():
    op.drop_table("orders")
