from functools import cache

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import UserRole

ROLE_TO_TEXT_MAP = {
    UserRole.ADMIN: "👑 Адмін",
    UserRole.MANAGER: "🗂️ Менеджер",
    UserRole.CLIENT: "👤 Клієнт",
}


@cache
def change_role_reply_kb(active_role: UserRole) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for role in UserRole:
        if role == active_role:
            continue
        builder.button(text=ROLE_TO_TEXT_MAP[role])
    return builder.adjust(2).as_markup(resize_keyboard=True, input_field_placeholder="Виберіть нову роль...")
