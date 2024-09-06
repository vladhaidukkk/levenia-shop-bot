from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SKIP_SURVEY_STEP_DATA = "skip_survey_step_data"


def build_skip_survey_step_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏭️ Пропустити", callback_data=SKIP_SURVEY_STEP_DATA)]]
    )
