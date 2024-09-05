import datetime as dt
from enum import StrEnum, auto

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class BonusType(StrEnum):
    DISCOUNT = auto()
    MONEY = auto()


class BonusUnit(StrEnum):
    PERCENTAGE = auto()
    AMOUNT = auto()


class BonusModel(ModelBase):
    id: Mapped[intpk]
    user_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    type: Mapped[BonusType]
    value: Mapped[int]
    unit: Mapped[BonusUnit]
    created_at: Mapped[created_at]
    applied_at: Mapped[dt.datetime | None]

    # Unfortunately Alembic doesn't detect CheckConstraints specified in mapped_column.
    # Therefore, we explicitly define them here at the table level.
    __table_args__ = (CheckConstraint("value > 0", name="value_positive"),)
