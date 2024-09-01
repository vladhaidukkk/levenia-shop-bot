from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import UserModel
from bot.errors import UserAlreadyExistsError


@inject_session
async def add_user(session: AsyncSession, tg_id: int) -> UserModel:
    try:
        new_user = UserModel(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except IntegrityError as error:
        raise UserAlreadyExistsError(tg_id=tg_id) from error
    else:
        return new_user
