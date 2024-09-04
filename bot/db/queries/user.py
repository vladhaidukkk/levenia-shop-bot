from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import UserModel, UserRole
from bot.errors import UserAlreadyExistsError, UserNotFoundError


@inject_session
async def add_user(session: AsyncSession, tg_id: int, username: str) -> UserModel:
    try:
        new_user = UserModel(tg_id=tg_id, username=username)
        session.add(new_user)
        await session.commit()
    except IntegrityError as error:
        raise UserAlreadyExistsError(tg_id=tg_id) from error
    else:
        return new_user


@inject_session
async def get_user(session: AsyncSession, tg_id: int) -> UserModel | None:
    query = select(UserModel).filter_by(tg_id=tg_id)
    return await session.scalar(query)


@inject_session
async def update_user(session: AsyncSession, tg_id: int, role: UserRole) -> UserModel:
    select_user_query = select(UserModel).filter_by(tg_id=tg_id)
    user = await session.scalar(select_user_query)
    if not user:
        raise UserNotFoundError(tg_id=tg_id)

    user.role = role
    await session.commit()
    return user
