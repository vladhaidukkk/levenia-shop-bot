import datetime as dt
from enum import StrEnum, auto

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class OrderStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    PREPARED = auto()
    SHIPPED = auto()
    REJECTED = auto()
    CANCELLED = auto()


class OrderModel(ModelBase):
    id: Mapped[intpk]
    user_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    manager_tg_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(server_default=OrderStatus.PENDING.name)
    created_at: Mapped[created_at]
    processed_at: Mapped[dt.datetime | None]
    rejected_at: Mapped[dt.datetime | None]
    cancelled_at: Mapped[dt.datetime | None]
