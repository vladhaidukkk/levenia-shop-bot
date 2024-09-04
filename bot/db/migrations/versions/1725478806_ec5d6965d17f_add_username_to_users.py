"""Add username to users.

Revision ID: ec5d6965d17f
Revises: 68dcee4c1c2f
Create Date: 2024-09-04 19:40:06.373855+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "ec5d6965d17f"
down_revision: str | None = "68dcee4c1c2f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(), nullable=False))
    op.create_unique_constraint(op.f("uq_users_username"), "users", ["username"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
    op.drop_column("users", "username")
