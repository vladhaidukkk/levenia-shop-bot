"""Create referrals table.

Revision ID: 9196f6e0c735
Revises: 03467f031394
Create Date: 2024-09-04 07:01:55.905308+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9196f6e0c735"
down_revision: str | None = "03467f031394"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "referrals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=False),
        sa.Column("referrer_tg_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["referrer_tg_id"], ["users.tg_id"], name=op.f("fk_referrals_referrer_tg_id_users")),
        sa.ForeignKeyConstraint(["user_tg_id"], ["users.tg_id"], name=op.f("fk_referrals_user_tg_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_referrals")),
        sa.UniqueConstraint("user_tg_id", name=op.f("uq_referrals_user_tg_id")),
    )


def downgrade() -> None:
    op.drop_table("referrals")
