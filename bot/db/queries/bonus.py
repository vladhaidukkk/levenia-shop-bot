from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import BonusModel, BonusType, BonusUnit


@inject_session
async def add_bonus(
    session: AsyncSession, user_tg_id: int, type_: BonusType, value: int, unit: BonusUnit
) -> BonusModel:
    new_bonus = BonusModel(user_tg_id=user_tg_id, type=type_, value=value, unit=unit)
    session.add(new_bonus)
    await session.commit()
    return new_bonus
