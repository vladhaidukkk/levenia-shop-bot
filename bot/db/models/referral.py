from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class ReferralModel(ModelBase):
    id: Mapped[intpk]
    user_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), unique=True)
    referrer_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    created_at: Mapped[created_at]
