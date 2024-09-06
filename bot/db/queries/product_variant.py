from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import ProductVariantModel
from bot.errors import ProductVariantAlreadyDeletedError, ProductVariantAlreadyExistsError, ProductVariantNotFoundError
from bot.utils import utcnow


@inject_session
async def add_product_variant(
    session: AsyncSession,
    *,
    product_id: int,
    creator_tg_id: int,
    image_id: str | None = None,
    color: str | None = None,
    size: str,
    quantity: int = 0,
) -> ProductVariantModel:
    try:
        new_product_variant = ProductVariantModel(
            product_id=product_id,
            creator_tg_id=creator_tg_id,
            image_id=image_id,
            color=color,
            size=size,
            quantity=quantity,
        )
        session.add(new_product_variant)
        await session.commit()
    except UniqueViolationError as error:
        raise ProductVariantAlreadyExistsError(product_id=product_id, color=color, size=size) from error
    else:
        return new_product_variant


@inject_session
async def delete_product_variant(session: AsyncSession, *, id_: int) -> None:
    select_product_variant_query = select(ProductVariantModel).filter_by(id=id_)
    product_variant = await session.scalar(select_product_variant_query)

    if not product_variant:
        raise ProductVariantNotFoundError(id_=id_)

    if product_variant.deleted_at:
        raise ProductVariantAlreadyDeletedError(id_=id_)

    product_variant.deleted_at = utcnow()
    await session.commit()
