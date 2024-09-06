from functools import cache

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import ProductGender

PRODUCT_GENDER_TO_TEXT_MAP = {
    ProductGender.MALE: "👔 Чоловічий",
    ProductGender.FEMALE: "👗 Жіночий",
    ProductGender.UNISEX: "🧥 Унісекс",
}

PRODUCT_GENDER_TO_DATA_MAP = {
    ProductGender.MALE: "male_product_gender",
    ProductGender.FEMALE: "female_product_gender",
    ProductGender.UNISEX: "unisex_product_gender",
}


@cache
def select_product_gender_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product_gender in ProductGender:
        builder.button(
            text=PRODUCT_GENDER_TO_TEXT_MAP[product_gender],
            callback_data=PRODUCT_GENDER_TO_DATA_MAP[product_gender],
        )
    return builder.adjust(2).as_markup()
