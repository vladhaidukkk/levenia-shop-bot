from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import ProductGender

PRODUCT_GENDER_TO_TEXT_MAP = {
    ProductGender.MALE: "👔 Чоловічий",
    ProductGender.FEMALE: "👗 Жіночий",
    ProductGender.UNISEX: "🧥 Унісекс",
}


def build_select_product_gender_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for product_gender in ProductGender:
        builder.button(text=PRODUCT_GENDER_TO_TEXT_MAP[product_gender])
    return builder.adjust(2).as_markup(resize_keyboard=True, input_field_placeholder="Виберіть гендер одягу...")
