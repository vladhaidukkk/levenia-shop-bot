from functools import cache

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import UserRole

ROLE_TO_TEXT_MAP = {
    UserRole.ADMIN: "👑 Адмін",
    UserRole.MANAGER: "🗂️ Менеджер",
    UserRole.CLIENT: "👤 Клієнт",
}

ROLE_TO_DATA_MAP = {
    UserRole.ADMIN: "👑 Адмін",
    UserRole.MANAGER: "🗂️ Менеджер",
    UserRole.CLIENT: "👤 Клієнт",
}


@cache
def change_role_inline_kb(active_role: UserRole) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for role in UserRole:
        if role == active_role:
            continue
        builder.button(text=ROLE_TO_TEXT_MAP[role], callback_data=ROLE_TO_DATA_MAP[role])
    return builder.adjust(2).as_markup()
