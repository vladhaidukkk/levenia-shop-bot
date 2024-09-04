from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import ReferralModel
from bot.errors import ReferralAlreadyExistsError


@inject_session
async def add_referral(session: AsyncSession, user_tg_id: int, referrer_tg_id: id, bonus_id: int) -> ReferralModel:
    try:
        new_referral = ReferralModel(user_tg_id=user_tg_id, referrer_tg_id=referrer_tg_id, bonus_id=bonus_id)
        session.add(new_referral)
        await session.commit()
    except IntegrityError as error:
        raise ReferralAlreadyExistsError(user_tg_id=user_tg_id) from error
    else:
        return new_referral
