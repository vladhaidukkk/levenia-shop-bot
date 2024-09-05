from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.user import get_user, update_user
from bot.filters import AdminFilter
from bot.keyboards.change_role import ROLE_TO_TEXT_MAP, build_change_role_keyboard
from bot.keyboards.root import RootKeyboardText, build_root_keyboard
from bot.utils import get_key_by_value

router = Router(name=__name__)
router.message.filter(AdminFilter())


class ChangeRoleSurvey(StatesGroup):
    user_tg_id = State()
    new_role = State()


@router.message(F.text == RootKeyboardText.CHANGE_ROLE)
async def change_role_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangeRoleSurvey.user_tg_id)
    await message.answer(
        "🪪 Введіть ID користувача, для якого ви хочете змінити роль:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ChangeRoleSurvey.user_tg_id)
async def change_role_survey_user_tg_id_handler(message: Message, state: FSMContext) -> None:
    try:
        user_tg_id = int(message.text)
    except ValueError:
        await message.answer("⚠️ Ви ввели неправильний ID користувача. Спробуйте ще раз:")
        return

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
        reply_markup=build_change_role_keyboard(active_role=user.role),
    )


@router.message(ChangeRoleSurvey.new_role, F.text.in_(ROLE_TO_TEXT_MAP.values()))
async def change_role_survey_new_role_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.update_data({"new_role": get_key_by_value(ROLE_TO_TEXT_MAP, message.text)})
    data = await state.get_data()

    updated_user = await update_user(tg_id=data["user_tg_id"], role=data["new_role"])
    if user.tg_id == updated_user.tg_id:
        user = updated_user
    else:
        await message.bot.send_message(
            chat_id=updated_user.tg_id,
            text=markdown.text(
                "🎭 Вашу роль було змінено. Тепер ви -",
                markdown.hbold(updated_user.role.value.capitalize()),
            ),
        )

    await state.clear()
    await message.answer(
        markdown.text(
            "✅ Роль для користувача",
            markdown.hcode(updated_user.tg_id),
            "успішно змінено.",
        ),
        reply_markup=build_root_keyboard(role=user.role),
    )


@router.message(ChangeRoleSurvey.new_role, ~F.text.in_(ROLE_TO_TEXT_MAP.values()))
async def change_role_survey_unknown_new_role_handler(message: Message, user: UserModel) -> None:
    await message.answer(
        "⚠️ Вказаної ролі не існує. Будь ласка, оберіть роль, натиснувши кнопку.",
        reply_markup=build_change_role_keyboard(active_role=user.role),
    )
