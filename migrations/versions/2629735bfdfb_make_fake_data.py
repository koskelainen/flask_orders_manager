"""make fake data

Revision ID: 2629735bfdfb
Revises: 0030c081cc93
Create Date: 2024-03-09 00:45:29.062907

"""
from alembic import op
from sqlalchemy import String
from sqlalchemy.sql import column, table

# revision identifiers, used by Alembic.
revision = "2629735bfdfb"
down_revision = "0030c081cc93"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from faker import Faker
    fake = Faker()
    my_table = table("orders",
                     column("name", String(300)),
                     column("address", String(300)),
                     )

    op.bulk_insert(my_table,
                   [{"name": fake.name(), "address": fake.address()} for _ in range(5)],
                   )


def downgrade() -> None:
    op.drop_table("orders")
