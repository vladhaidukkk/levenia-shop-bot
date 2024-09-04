"""Create bonuses table.

Revision ID: a3b4d62e6d60
Revises: 9196f6e0c735
Create Date: 2024-09-04 18:56:21.795275+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a3b4d62e6d60"
down_revision: str | None = "9196f6e0c735"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

bonus_type_enum = sa.Enum("DISCOUNT", "MONEY", name="bonus_type")
bonus_unit_enum = sa.Enum("PERCENTAGE", "FIXED_AMOUNT", name="bonus_unit")


def upgrade() -> None:
    op.create_table(
        "bonuses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=False),
        sa.Column("type", bonus_type_enum, nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("unit", bonus_unit_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("applied_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("value > 0", name=op.f("ck_bonuses_value_positive")),
        sa.ForeignKeyConstraint(["user_tg_id"], ["users.tg_id"], name=op.f("fk_bonuses_user_tg_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bonuses")),
    )


def downgrade() -> None:
    op.drop_table("bonuses")
    bonus_type_enum.drop(op.get_bind())
    bonus_unit_enum.drop(op.get_bind())
