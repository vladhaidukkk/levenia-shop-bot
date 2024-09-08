"""Create orders table.

Revision ID: a198d5bd956d
Revises: bed5eff38809
Create Date: 2024-09-08 20:32:05.885526+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a198d5bd956d"
down_revision: str | None = "bed5eff38809"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

order_status_enum = sa.Enum(
    "PENDING", "PROCESSING", "PREPARED", "SHIPPED", "REJECTED", "CANCELLED", name="order_status"
)


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("manager_tg_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "status",
            order_status_enum,
            server_default="PENDING",
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("rejected_at", sa.DateTime(), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["manager_tg_id"], ["users.id"], name=op.f("fk_orders_manager_tg_id_users")),
        sa.ForeignKeyConstraint(["user_tg_id"], ["users.id"], name=op.f("fk_orders_user_tg_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )


def downgrade() -> None:
    op.drop_table("orders")
    order_status_enum.drop(op.get_bind())
