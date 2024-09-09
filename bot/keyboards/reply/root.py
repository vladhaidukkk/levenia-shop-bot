from enum import StrEnum
from functools import cache

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import UserRole


class RootKeyboardText(StrEnum):
    CHANGE_ROLE = "🎭 Змінити Роль"
    ADD_PRODUCT = "🆕 Додати Новий Одяг"
    ADD_PRODUCT_VARIANT = "➕ Додати Варіант Одягу"
    DELETE_PRODUCT = "🗑️ Видалити Одяг"
    DELETE_PRODUCT_VARIANT = "➖️ Видалити Варіант Одягу"
    LIST_CATEGORIES = "🏷️ Список Категорій"
    LIST_BRANDS = "🏢 Список Брендів"
    LIST_MATERIALS = "🧵 Список Матеріалів"
    INVITE_FRIEND = "🔗 Запросити Друга"


@cache
def root_reply_kb(role: UserRole) -> ReplyKeyboardMarkup:
    client_actions = [RootKeyboardText.INVITE_FRIEND]
    manager_actions = [
        RootKeyboardText.ADD_PRODUCT,
        RootKeyboardText.ADD_PRODUCT_VARIANT,
        RootKeyboardText.DELETE_PRODUCT,
        RootKeyboardText.DELETE_PRODUCT_VARIANT,
        RootKeyboardText.LIST_CATEGORIES,
        RootKeyboardText.LIST_BRANDS,
        RootKeyboardText.LIST_MATERIALS,
        *client_actions,
    ]
    admin_actions = [RootKeyboardText.CHANGE_ROLE, *manager_actions]
    role_to_actions_map = {
        UserRole.ADMIN: admin_actions,
        UserRole.MANAGER: manager_actions,
        UserRole.CLIENT: client_actions,
    }

    builder = ReplyKeyboardBuilder()
    for action in role_to_actions_map[role]:
        builder.button(text=action)

    markup = builder.adjust(2).as_markup(resize_keyboard=True, input_field_placeholder="Виберіть дію...")
    return markup if markup.keyboard else ReplyKeyboardRemove()
