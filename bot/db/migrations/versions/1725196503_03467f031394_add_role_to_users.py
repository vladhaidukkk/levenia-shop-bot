"""Add role to users.

Revision ID: 03467f031394
Revises: c4ec56b2b889
Create Date: 2024-09-01 13:15:03.606871+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "03467f031394"
down_revision: str | None = "c4ec56b2b889"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role_enum = sa.Enum("ADMIN", "MANAGER", "CLIENT", name="user_role")


def upgrade() -> None:
    # We must create the type first because the server_default value is specified.
    user_role_enum.create(op.get_bind())
    op.add_column(
        "users",
        sa.Column("role", user_role_enum, server_default="CLIENT", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "role")
    user_role_enum.drop(op.get_bind())
