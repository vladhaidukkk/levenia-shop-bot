from enum import StrEnum

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import UserRole


class RootKeyboardText(StrEnum):
    CHANGE_ROLE = "🎭 Змінити Роль"


def build_root_keyboard(role: UserRole) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    if role == UserRole.ADMIN:
        builder.button(text=RootKeyboardText.CHANGE_ROLE)
    return builder.adjust(2).as_markup(resize_keyboard=True, input_field_placeholder="Виберіть дію...")
