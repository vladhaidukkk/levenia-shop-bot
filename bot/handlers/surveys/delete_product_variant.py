from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.product_variant import delete_product_variant
from bot.errors import ProductVariantAlreadyDeletedError, ProductVariantNotFoundError
from bot.filters.role import ManagerFilter
from bot.keyboards.reply.cancel_survey import cancel_survey_reply_kb
from bot.keyboards.reply.root import RootKeyboardText, root_reply_kb

router = Router(name=__name__)
router.message.filter(ManagerFilter())


class DeleteProductVariantSurvey(StatesGroup):
    product_variant_id = State()


@router.message(F.text == RootKeyboardText.DELETE_PRODUCT_VARIANT)
async def delete_product_variant_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteProductVariantSurvey.product_variant_id)
    await message.answer(
        "🆔️ Введіть ID варіанту одягу, який ви хочете видалити:", reply_markup=cancel_survey_reply_kb()
    )


@router.message(DeleteProductVariantSurvey.product_variant_id, F.text.regexp(r"^\d+$"))
async def delete_product_variant_survey_product_variant_id_handler(
    message: Message, state: FSMContext, user: UserModel
) -> None:
    await state.update_data({"product_variant_id": int(message.text)})
    data = await state.get_data()

    try:
        await delete_product_variant(id_=data["product_variant_id"])
    except ProductVariantNotFoundError:
        await message.answer("⚠️ Варіант одягу з таким ID не існує. Спродуйте ще раз:")
        return
    except ProductVariantAlreadyDeletedError:
        await message.answer("⚠️ Варіант одяг з цим ID вже видалено. Введіть інший ID:")
        return

    await state.clear()
    await message.answer(
        markdown.text(
            "🗑️ Варіант одягу з ID:",
            markdown.hcode(data["product_variant_id"]),
            "видалено. Ви можете відновити його будь-коли.",
        ),
        reply_markup=root_reply_kb(role=user.role),
    )


@router.message(DeleteProductVariantSurvey.product_variant_id, ~F.text.regexp(r"^\d+$"))
async def delete_product_variant_survey_invalid_product_variant_id_handler(message: Message) -> None:
    await message.answer("⚠️ ID варіанту одягу вміщає лише цифри. Введіть значення ще раз:")
