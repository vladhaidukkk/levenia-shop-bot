from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.product import get_product
from bot.db.queries.product_variant import add_product_variant
from bot.errors import ProductVariantAlreadyExistsError
from bot.filters.role import ManagerFilter
from bot.keyboards.inline.skip_survey_step import SKIP_SURVEY_STEP_DATA, skip_survey_step_inline_kb
from bot.keyboards.reply.cancel_survey import cancel_survey_reply_kb
from bot.keyboards.reply.root import RootKeyboardText, root_reply_kb

router = Router(name=__name__)
router.message.filter(ManagerFilter())
router.callback_query.filter(ManagerFilter())


class AddProductVariantSurvey(StatesGroup):
    product_id = State()
    image_id = State()
    color = State()
    size = State()
    quantity = State()


@router.message(F.text == RootKeyboardText.ADD_PRODUCT_VARIANT)
async def add_product_variant_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProductVariantSurvey.product_id)
    await message.answer(
        "🆔️ Введіть ID одягу, для якого ви хочете добавити варіант:",
        reply_markup=cancel_survey_reply_kb(),
    )


@router.message(AddProductVariantSurvey.product_id, F.text.regexp(r"^\d+$"))
async def add_product_variant_survey_product_id_handler(message: Message, state: FSMContext) -> None:
    product_id = int(message.text)
    product = await get_product(id_=product_id)
    if not product:
        await message.answer("⚠️ Одягу з таким ID не існує. Спробуйте ще раз:")
        return

    await state.update_data({"product_id": product_id})
    await state.set_state(AddProductVariantSurvey.image_id)
    await message.answer("🖼️ Завантажте зображення варіанту:", reply_markup=skip_survey_step_inline_kb())


@router.message(AddProductVariantSurvey.product_id, ~F.text.regexp(r"^\d+$"))
async def add_product_variant_survey_invalid_product_id_handler(message: Message) -> None:
    await message.answer("⚠️ Ви ввели неправильний ID одягу. Спробуйте ще раз:")


@router.message(AddProductVariantSurvey.image_id, F.photo)
async def add_product_variant_survey_image_id_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"image_id": message.photo[-1].file_id})
    await state.set_state(AddProductVariantSurvey.color)
    await message.answer("🎨 Вкажіть колір цього варіанту:", reply_markup=skip_survey_step_inline_kb())


@router.message(AddProductVariantSurvey.image_id, ~F.photo)
async def add_product_variant_survey_invalid_image_id_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно надіслати саме фото, а не щось інше. Спробуйте ще раз:")


@router.callback_query(AddProductVariantSurvey.image_id, F.data == SKIP_SURVEY_STEP_DATA)
async def add_product_variant_survey_skip_image_id_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"image_id": None})
    await state.set_state(AddProductVariantSurvey.color)
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer("🎨 Вкажіть колір цього варіанту:", reply_markup=skip_survey_step_inline_kb())


@router.message(AddProductVariantSurvey.color, F.text)
async def add_product_variant_survey_color_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"color": message.text})
    await state.set_state(AddProductVariantSurvey.size)
    await message.answer("️📏 Вкажіть розмір цього варіанту:")


@router.message(AddProductVariantSurvey.color, ~F.text)
async def add_product_variant_survey_invalid_color_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно ввести саме текст, а не щось інше. Спробуйте ще раз:")


@router.callback_query(AddProductVariantSurvey.color, F.data == SKIP_SURVEY_STEP_DATA)
async def add_product_variant_survey_skip_color_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"color": None})
    await state.set_state(AddProductVariantSurvey.size)
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer("️📏 Вкажіть розмір цього варіанту:")


@router.message(AddProductVariantSurvey.size, F.text)
async def add_product_variant_survey_size_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"size": message.text})
    await state.set_state(AddProductVariantSurvey.quantity)
    await message.answer("🔢 Вкажіть наявну кількість цього варіанту:")


@router.message(AddProductVariantSurvey.size, ~F.text)
async def add_product_variant_survey_invalid_size_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно ввести саме текст, а не щось інше. Спробуйте ще раз:")


@router.message(AddProductVariantSurvey.quantity, F.text.regexp(r"^\d+$"))
async def add_product_variant_survey_quantity_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.update_data({"quantity": int(message.text)})
    data = await state.get_data()

    try:
        product_variant = await add_product_variant(
            product_id=data["product_id"],
            creator_tg_id=user.tg_id,
            image_id=data["image_id"],
            color=data["color"],
            size=data["size"],
            quantity=data["quantity"],
        )
    except ProductVariantAlreadyExistsError:
        await message.answer(
            (
                "⛔ Варіант з такою комбінацією кольору та розміру для цього одягу вже існує. "
                "Додайте інший варіант якщо потрібно."
            ),
            reply_markup=root_reply_kb(role=user.role),
        )
    else:
        await message.answer(
            markdown.text(
                "✅ Варіант одягу успішно доданий до каталогу.",
                f"Ось його ID: {markdown.hcode(product_variant.id)}.",
            ),
            reply_markup=root_reply_kb(role=user.role),
        )
    finally:
        await state.clear()


@router.message(AddProductVariantSurvey.quantity, ~F.text.regexp(r"^\d+$"))
async def add_product_variant_survey_invalid_quantity_handler(message: Message) -> None:
    await message.answer("⚠️ Кількість повинна бути вказана числом. Введіть значення ще раз:")
