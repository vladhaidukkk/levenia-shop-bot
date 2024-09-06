from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.product import add_product
from bot.filters.role import ManagerFilter
from bot.keyboards.inline.skip_survey_step import SKIP_SURVEY_STEP_DATA, skip_survey_step_inline_kb
from bot.keyboards.reply.root import RootKeyboardText, root_reply_kb
from bot.keyboards.reply.select_product_gender import (
    PRODUCT_GENDER_TO_TEXT_MAP,
    select_product_gender_reply_kb,
)
from bot.utils import get_key_by_value

router = Router(name=__name__)
router.message.filter(ManagerFilter())
router.callback_query.filter(ManagerFilter())


class AddProductSurvey(StatesGroup):
    name = State()
    image_id = State()
    gender = State()
    category = State()
    price = State()


@router.message(F.text == RootKeyboardText.ADD_PRODUCT)
async def add_product_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProductSurvey.name)
    await message.answer("📝 Введіть назву одягу:", reply_markup=ReplyKeyboardRemove())


@router.message(AddProductSurvey.name, F.text)
async def add_product_survey_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"name": message.text})
    await state.set_state(AddProductSurvey.image_id)
    await message.answer("🖼️ Завантажте зображення одягу:", reply_markup=skip_survey_step_inline_kb())


@router.message(AddProductSurvey.name, ~F.text)
async def add_product_survey_invalid_name_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно ввести саме текст, а не щось інше. Спробуйте ще раз:")


@router.message(AddProductSurvey.image_id, F.photo)
async def add_product_survey_image_id_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"image_id": message.photo[-1].file_id})
    await state.set_state(AddProductSurvey.gender)
    await message.answer(
        "🚻 Оберіть гендер одягу, натиснувши кнопку.",
        reply_markup=select_product_gender_reply_kb(),
    )


@router.message(AddProductSurvey.image_id, ~F.photo)
async def add_product_survey_invalid_image_id_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно надіслати саме фото, а не щось інше. Спробуйте ще раз:")


@router.callback_query(AddProductSurvey.image_id, F.data == SKIP_SURVEY_STEP_DATA)
async def add_product_survey_skip_image_id_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"image_id": None})
    await state.set_state(AddProductSurvey.gender)
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer(
        "🚻 Оберіть гендер одягу, натиснувши кнопку.",
        reply_markup=select_product_gender_reply_kb(),
    )


@router.message(AddProductSurvey.gender, F.text.in_(PRODUCT_GENDER_TO_TEXT_MAP.values()))
async def add_product_survey_gender_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"gender": get_key_by_value(PRODUCT_GENDER_TO_TEXT_MAP, message.text)})
    await state.set_state(AddProductSurvey.category)
    await message.answer("🏷️ Введіть категорію одягу:", reply_markup=ReplyKeyboardRemove())


@router.message(AddProductSurvey.gender, ~F.text.in_(PRODUCT_GENDER_TO_TEXT_MAP.values()))
async def add_product_survey_unknown_gender_handler(message: Message) -> None:
    await message.answer(
        "⚠️ Вказаного гендеру не існує. Будь ласка, оберіть гендер одягу, натиснувши кнопку.",
        reply_markup=select_product_gender_reply_kb(),
    )


@router.message(AddProductSurvey.category, F.text)
async def add_product_survey_category_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"category": message.text})
    await state.set_state(AddProductSurvey.price)
    await message.answer("💵 Вкажіть ціну одягу в гривнях:")


@router.message(AddProductSurvey.category, ~F.text)
async def add_product_survey_invalid_category_handler(message: Message) -> None:
    await message.answer("⚠️ Вам необхідно ввести саме текст, а не щось інше. Спробуйте ще раз:")


@router.message(AddProductSurvey.price, F.text.regexp(r"^[1-9][0-9]*$"))
async def add_product_survey_price_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.update_data({"price": int(message.text)})
    data = await state.get_data()

    product = await add_product(
        creator_tg_id=user.tg_id,
        name=data["name"],
        image_id=data["image_id"],
        gender=data["gender"],
        category=data["category"],
        price=data["price"],
    )

    await state.clear()
    await message.answer(
        markdown.text(
            "✅ Одяг успішно доданий до каталогу.",
            f"Ось його ID: {markdown.hcode(product.id)}.",
        ),
        reply_markup=root_reply_kb(role=user.role),
    )


@router.message(AddProductSurvey.price, ~F.text.regexp(r"^[1-9][0-9]*$"))
async def add_product_survey_invalid_price_handler(message: Message) -> None:
    await message.answer("⚠️ Ціна може складатися лише з цифр. Введіть значення ще раз:")
