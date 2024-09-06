from functools import cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SKIP_SURVEY_STEP_DATA = "skip_survey_step_data"


@cache
def skip_survey_step_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏭️ Пропустити", callback_data=SKIP_SURVEY_STEP_DATA)]]
    )
