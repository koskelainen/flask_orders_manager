"""add extension pg_stat_statements

Revision ID: e6fcc046e6ee
Revises: 2629735bfdfb
Create Date: 2024-03-18 12:27:52.066584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6fcc046e6ee'
down_revision = '2629735bfdfb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_stat_statements")
