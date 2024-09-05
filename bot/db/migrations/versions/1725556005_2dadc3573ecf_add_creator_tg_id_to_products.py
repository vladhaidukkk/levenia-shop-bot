"""Add creator_tg_id to products.

Revision ID: 2dadc3573ecf
Revises: ca423088bd92
Create Date: 2024-09-05 17:06:45.245275+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "2dadc3573ecf"
down_revision: str | None = "ca423088bd92"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("products", sa.Column("creator_tg_id", sa.BigInteger(), nullable=False))
    op.create_foreign_key(op.f("fk_products_creator_tg_id_users"), "products", "users", ["creator_tg_id"], ["tg_id"])


def downgrade() -> None:
    op.drop_constraint(op.f("fk_products_creator_tg_id_users"), "products", type_="foreignkey")
    op.drop_column("products", "creator_tg_id")
