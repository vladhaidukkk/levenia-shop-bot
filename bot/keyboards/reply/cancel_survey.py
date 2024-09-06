from functools import cache

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CANCEL_SURVEY_TEXT = "🚫 Скасувати Дію"


@cache
def cancel_survey_reply_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=CANCEL_SURVEY_TEXT)]], resize_keyboard=True)
