"""Add bonus_id to referrals.

Revision ID: 68dcee4c1c2f
Revises: a3b4d62e6d60
Create Date: 2024-09-04 19:20:42.514394+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "68dcee4c1c2f"
down_revision: str | None = "a3b4d62e6d60"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("referrals", sa.Column("bonus_id", sa.Integer(), nullable=False))
    op.create_unique_constraint(op.f("uq_referrals_bonus_id"), "referrals", ["bonus_id"])
    op.create_foreign_key(op.f("fk_referrals_bonus_id_bonuses"), "referrals", "bonuses", ["bonus_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("fk_referrals_bonus_id_bonuses"), "referrals", type_="foreignkey")
    op.drop_constraint(op.f("uq_referrals_bonus_id"), "referrals", type_="unique")
    op.drop_column("referrals", "bonus_id")
