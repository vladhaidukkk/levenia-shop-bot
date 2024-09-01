from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    created_at: Mapped[created_at]
