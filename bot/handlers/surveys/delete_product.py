from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.product import delete_product
from bot.errors import ProductAlreadyDeletedError, ProductNotFoundError
from bot.filters import ManagerFilter
from bot.keyboards.root import RootKeyboardText, build_root_keyboard

router = Router(name=__name__)
router.message.filter(ManagerFilter())


class DeleteProductSurvey(StatesGroup):
    product_id = State()


@router.message(F.text == RootKeyboardText.DELETE_PRODUCT)
async def delete_product_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteProductSurvey.product_id)
    await message.answer("🆔️ Введіть ID одягу, який ви хочете видалити:", reply_markup=ReplyKeyboardRemove())


@router.message(DeleteProductSurvey.product_id, F.text.regexp(r"^\d+$"))
async def delete_product_survey_product_id_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.update_data({"product_id": int(message.text)})
    data = await state.get_data()

    try:
        await delete_product(id_=data["product_id"])
    except ProductNotFoundError:
        await message.answer("⚠️ Одягу з таким ID не існує. Спродуйте ще раз:")
        return
    except ProductAlreadyDeletedError:
        await message.answer("⚠️ Одяг з цим ID вже видалено. Введіть інший ID:")
        return

    await state.clear()
    await message.answer(
        markdown.text(
            "🗑️ Одяг з ID:",
            markdown.hcode(data["product_id"]),
            "видалено. Ви можете відновити його будь-коли.",
        ),
        reply_markup=build_root_keyboard(role=user.role),
    )


@router.message(DeleteProductSurvey.product_id, ~F.text.regexp(r"^\d+$"))
async def delete_product_survey_invalid_product_id_handler(message: Message) -> None:
    await message.answer("⚠️ ID одягу вміщає лише цифри. Введіть значення ще раз:")
