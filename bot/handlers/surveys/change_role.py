from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.user import get_user, update_user
from bot.filters.role import AdminFilter
from bot.keyboards.inline.change_role import ROLE_TO_DATA_MAP, ROLE_TO_TEXT_MAP, change_role_inline_kb
from bot.keyboards.reply.cancel_survey import cancel_survey_reply_kb
from bot.keyboards.reply.root import RootKeyboardText, root_reply_kb
from bot.utils import get_key_by_value

router = Router(name=__name__)
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


class ChangeRoleSurvey(StatesGroup):
    user_tg_id = State()
    new_role = State()


@router.message(F.text == RootKeyboardText.CHANGE_ROLE)
async def change_role_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangeRoleSurvey.user_tg_id)
    await message.answer(
        "🪪 Введіть ID користувача, для якого ви хочете змінити роль:",
        reply_markup=cancel_survey_reply_kb(),
    )


@router.message(ChangeRoleSurvey.user_tg_id, F.text.regexp(r"^\d+$"))
async def change_role_survey_user_tg_id_handler(message: Message, state: FSMContext) -> None:
    user_tg_id = int(message.text)
    user = await get_user(tg_id=user_tg_id)
    if not user:
        await message.answer("⚠️ Користувача з таким ID не існує. Спробуйте ще раз:")
        return

    await state.update_data({"user_tg_id": user_tg_id})
    await state.set_state(ChangeRoleSurvey.new_role)
    await message.answer(
        markdown.text(
            "️🔍 Поточна роль користувача:",
            f"{markdown.hbold(user.role.value.capitalize())}.",
            "Оберіть нову роль, натиснувши кнопку.",
        ),
        reply_markup=change_role_inline_kb(active_role=user.role),
    )


@router.message(ChangeRoleSurvey.user_tg_id, ~F.text.regexp(r"^\d+$"))
async def change_role_survey_invalid_user_tg_id_handler(message: Message) -> None:
    await message.answer("⚠️ Ви ввели неправильний ID користувача. Спробуйте ще раз:")


@router.callback_query(ChangeRoleSurvey.new_role, F.data.in_(ROLE_TO_DATA_MAP.values()))
async def change_role_survey_new_role_handler(
    callback_query: CallbackQuery, state: FSMContext, user: UserModel
) -> None:
    new_role = get_key_by_value(ROLE_TO_DATA_MAP, callback_query.data)
    await state.update_data({"new_role": new_role})
    data = await state.get_data()

    updated_user = await update_user(tg_id=data["user_tg_id"], role=data["new_role"])
    if user.tg_id == updated_user.tg_id:
        user = updated_user
    else:
        await callback_query.message.bot.send_message(
            chat_id=updated_user.tg_id,
            text=markdown.text(
                "🎭 Вашу роль було змінено. Тепер ви -",
                f"{markdown.hbold(updated_user.role.value.capitalize())}.",
            ),
        )

    await state.clear()
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(ROLE_TO_TEXT_MAP[new_role])
    await callback_query.message.answer(
        markdown.text(
            "✅ Роль для користувача",
            markdown.hcode(updated_user.tg_id),
            "успішно змінено.",
        ),
        reply_markup=root_reply_kb(role=user.role),
    )


@router.message(ChangeRoleSurvey.new_role)
async def change_role_survey_unknown_new_role_handler(message: Message) -> None:
    await message.answer("⚠️ Будь ласка, оберіть нову роль, натиснувши кнопку під повідомленням.")
