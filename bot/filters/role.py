from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from bot.db.models import UserModel, UserRole


class RoleFilter(Filter):
    def __init__(self, *roles: UserRole) -> None:
        self.roles = set(roles)

    async def __call__(self, _event: Message | CallbackQuery, user: UserModel | None) -> bool:
        return user and user.role in self.roles


class AdminFilter(RoleFilter):
    def __init__(self) -> None:
        super().__init__(UserRole.ADMIN)


class ManagerFilter(RoleFilter):
    def __init__(self) -> None:
        super().__init__(UserRole.MANAGER, UserRole.ADMIN)
