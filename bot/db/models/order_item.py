from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at, intpk

from .base import ModelBase


class OrderItemModel(ModelBase):
    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variants.id"))
    quantity: Mapped[int]
    unit_price: Mapped[int]
    created_at: Mapped[created_at]
