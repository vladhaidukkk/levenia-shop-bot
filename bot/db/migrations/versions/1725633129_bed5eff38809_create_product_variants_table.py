"""Create product_variants table.

Revision ID: bed5eff38809
Revises: 90d44a643657
Create Date: 2024-09-06 14:32:09.356819+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "bed5eff38809"
down_revision: str | None = "90d44a643657"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "product_variants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("creator_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("image_id", sa.String(), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("size", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("quantity >= 0", name=op.f("ck_product_variants_quantity_non_negative")),
        sa.ForeignKeyConstraint(
            ["creator_tg_id"], ["users.tg_id"], name=op.f("fk_product_variants_creator_tg_id_users")
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], name=op.f("fk_product_variants_product_id_products")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_variants")),
        sa.UniqueConstraint(
            "color", "size", name=op.f("uq_product_variants_color_size"), postgresql_nulls_not_distinct=True
        ),
    )


def downgrade() -> None:
    op.drop_table("product_variants")
