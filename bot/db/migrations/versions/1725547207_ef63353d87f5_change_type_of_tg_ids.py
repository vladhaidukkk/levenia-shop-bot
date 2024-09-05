"""Change type of tg_ids.

Revision ID: ef63353d87f5
Revises: ec5d6965d17f
Create Date: 2024-09-05 14:40:07.494616+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "ef63353d87f5"
down_revision: str | None = "ec5d6965d17f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("bonuses", "user_tg_id", existing_type=sa.INTEGER(), type_=sa.BigInteger(), existing_nullable=False)
    op.alter_column(
        "referrals", "user_tg_id", existing_type=sa.INTEGER(), type_=sa.BigInteger(), existing_nullable=False
    )
    op.alter_column(
        "referrals", "referrer_tg_id", existing_type=sa.INTEGER(), type_=sa.BigInteger(), existing_nullable=False
    )
    op.alter_column("users", "tg_id", existing_type=sa.INTEGER(), type_=sa.BigInteger(), existing_nullable=False)


def downgrade() -> None:
    op.alter_column("users", "tg_id", existing_type=sa.BigInteger(), type_=sa.INTEGER(), existing_nullable=False)
    op.alter_column(
        "referrals", "referrer_tg_id", existing_type=sa.BigInteger(), type_=sa.INTEGER(), existing_nullable=False
    )
    op.alter_column(
        "referrals", "user_tg_id", existing_type=sa.BigInteger(), type_=sa.INTEGER(), existing_nullable=False
    )
    op.alter_column("bonuses", "user_tg_id", existing_type=sa.BigInteger(), type_=sa.INTEGER(), existing_nullable=False)
