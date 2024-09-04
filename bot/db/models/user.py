from enum import StrEnum, auto

from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class UserRole(StrEnum):
    ADMIN = auto()
    MANAGER = auto()
    CLIENT = auto()


class UserModel(ModelBase):
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRole] = mapped_column(server_default=UserRole.CLIENT.name)
    created_at: Mapped[created_at]
