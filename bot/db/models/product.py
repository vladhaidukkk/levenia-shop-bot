from enum import StrEnum, auto

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class ProductGender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    UNISEX = auto()


class ProductModel(ModelBase):
    id: Mapped[intpk]
    name: Mapped[str]
    image_id: Mapped[str | None]
    description: Mapped[str | None]
    gender: Mapped[ProductGender]
    category: Mapped[str]
    brand: Mapped[str | None]
    material: Mapped[str | None]
    price: Mapped[int]
    created_at: Mapped[created_at]

    __table_args__ = (CheckConstraint("price > 0", name="price_positive"),)
