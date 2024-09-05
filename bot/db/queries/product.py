from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import ProductGender, ProductModel


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
