import datetime as dt

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class ProductVariantModel(ModelBase):
    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    creator_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    image_id: Mapped[str | None]
    color: Mapped[str | None]
    size: Mapped[str]
    quantity: Mapped[int]
    created_at: Mapped[created_at]
    deleted_at: Mapped[dt.datetime | None]

    __table_args__ = (
        UniqueConstraint("color", "size", postgresql_nulls_not_distinct=True),
        CheckConstraint("quantity >= 0", name="quantity_non_negative"),
    )
