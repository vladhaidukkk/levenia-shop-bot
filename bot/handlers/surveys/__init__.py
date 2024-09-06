from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db.models import UserModel
from bot.keyboards.reply.cancel_survey import CANCEL_SURVEY_TEXT
from bot.keyboards.reply.root import root_reply_kb

from .add_product import router as add_product_survey_router
from .change_role import router as change_role_survey_router
from .delete_product import router as delete_product_survey_router

router = Router(name=__name__)


@router.message(Command("cancel"))
@router.message(F.text == CANCEL_SURVEY_TEXT)
async def cancel_command_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.clear()
    await message.answer("🚫 Поточну дію скасовано.", reply_markup=root_reply_kb(role=user.role))


router.include_routers(change_role_survey_router, add_product_survey_router, delete_product_survey_router)
