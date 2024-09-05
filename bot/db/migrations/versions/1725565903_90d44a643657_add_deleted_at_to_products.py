"""Add deleted_at to products.

Revision ID: 90d44a643657
Revises: 2dadc3573ecf
Create Date: 2024-09-05 19:51:43.067141+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "90d44a643657"
down_revision: str | None = "2dadc3573ecf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("products", sa.Column("deleted_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("products", "deleted_at")
