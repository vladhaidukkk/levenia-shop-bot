from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import ProductGender, ProductModel
from bot.errors import ProductAlreadyDeletedError, ProductNotFoundError
from bot.utils import utcnow


@inject_session
async def add_product(
    session: AsyncSession,
    *,
    creator_tg_id: int,
    name: str,
    image_id: str | None = None,
    description: str | None = None,
    gender: ProductGender,
    category: str,
    brand: str | None = None,
    material: str | None = None,
    price: int,
) -> ProductModel:
    new_product = ProductModel(
        creator_tg_id=creator_tg_id,
        name=name,
        image_id=image_id,
        description=description,
        gender=gender,
        category=category,
        brand=brand,
        material=material,
        price=price,
    )
    session.add(new_product)
    await session.commit()
    return new_product


@inject_session
async def get_product(session: AsyncSession, *, id_: int) -> ProductModel | None:
    query = select(ProductModel).filter_by(id=id_)
    return await session.scalar(query)


@inject_session
async def get_product_categories(session: AsyncSession) -> list[str]:
    query = (
        select(func.lower(ProductModel.category))
        .group_by(func.lower(ProductModel.category))
        .order_by(func.lower(ProductModel.category))
    )
    result = await session.scalars(query)
    return list(result.all())


@inject_session
async def get_product_brands(session: AsyncSession) -> list[str]:
    query = (
        select(func.lower(ProductModel.brand))
        .group_by(func.lower(ProductModel.brand))
        .order_by(func.lower(ProductModel.brand))
    )
    result = await session.scalars(query)
    return list(result.all())


@inject_session
async def get_product_materials(session: AsyncSession) -> list[str]:
    query = (
        select(func.lower(ProductModel.material))
        .group_by(func.lower(ProductModel.material))
        .order_by(func.lower(ProductModel.material))
    )
    result = await session.scalars(query)
    return list(result.all())


@inject_session
async def delete_product(session: AsyncSession, *, id_: int) -> None:
    select_product_query = select(ProductModel).filter_by(id=id_)
    product = await session.scalar(select_product_query)

    if not product:
        raise ProductNotFoundError(id_=id_)

    if product.deleted_at:
        raise ProductAlreadyDeletedError(id_=id_)

    product.deleted_at = utcnow()
    await session.commit()
