from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from bot.db.models import UserModel, UserRole


class AdminFilter(Filter):
    async def __call__(self, _event: Message | CallbackQuery, user: UserModel | None) -> bool:
        return user and user.role == UserRole.ADMIN


class ManagerFilter(Filter):
    async def __call__(self, _message: Message | CallbackQuery, user: UserModel | None) -> bool:
        return user and user.role in {UserRole.MANAGER, UserRole.ADMIN}
