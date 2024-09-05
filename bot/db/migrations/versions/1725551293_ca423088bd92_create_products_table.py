"""Create products table.

Revision ID: ca423088bd92
Revises: ef63353d87f5
Create Date: 2024-09-05 15:48:13.108790+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "ca423088bd92"
down_revision: str | None = "ef63353d87f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

product_gender_enum = sa.Enum("MALE", "FEMALE", "UNISEX", name="product_gender")


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_id", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("gender", product_gender_enum, nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("material", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("price > 0", name=op.f("ck_products_price_positive")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )


def downgrade() -> None:
    op.drop_table("products")
    product_gender_enum.drop(op.get_bind())
