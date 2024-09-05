from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.product import add_product
from bot.filters import ManagerFilter
from bot.keyboards.root import RootKeyboardText, build_root_keyboard
from bot.keyboards.select_product_gender import PRODUCT_GENDER_TO_TEXT_MAP, build_select_product_gender_keyboard
from bot.utils import get_key_by_value

router = Router(name=__name__)
router.message.filter(ManagerFilter())


class AddProductSurvey(StatesGroup):
    name = State()
    gender = State()
    category = State()
    price = State()


@router.message(F.text == RootKeyboardText.ADD_PRODUCT)
async def add_product_button_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProductSurvey.name)
    await message.answer(text="📝 Введіть назву одягу:", reply_markup=ReplyKeyboardRemove())


@router.message(AddProductSurvey.name)
async def add_product_survey_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"name": message.text})
    await state.set_state(AddProductSurvey.gender)
    await message.answer(
        text="🚻 Оберіть гендер одягу, натиснувши кнопку.",
        reply_markup=build_select_product_gender_keyboard(),
    )


@router.message(AddProductSurvey.gender, F.text.in_(PRODUCT_GENDER_TO_TEXT_MAP.values()))
async def add_product_survey_gender_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"gender": get_key_by_value(PRODUCT_GENDER_TO_TEXT_MAP, message.text)})
    await state.set_state(AddProductSurvey.category)
    await message.answer(text="🏷️ Введіть категорію одягу:", reply_markup=ReplyKeyboardRemove())


@router.message(AddProductSurvey.gender, ~F.text.in_(PRODUCT_GENDER_TO_TEXT_MAP.values()))
async def add_product_survey_unknown_gender_handler(message: Message) -> None:
    await message.answer(
        text="⚠️ Вказаного гендеру не існує. Будь ласка, оберіть гендер одягу, натиснувши кнопку.",
        reply_markup=build_select_product_gender_keyboard(),
    )


@router.message(AddProductSurvey.category)
async def add_product_survey_category_handler(message: Message, state: FSMContext) -> None:
    await state.update_data({"category": message.text})
    await state.set_state(AddProductSurvey.price)
    await message.answer(text="💵 Вкажіть ціну одягу в гривнях:")


@router.message(AddProductSurvey.price, F.text.regexp(r"^[1-9][0-9]*$"))
async def add_product_survey_price_handler(message: Message, state: FSMContext, user: UserModel) -> None:
    await state.update_data({"price": int(message.text)})
    data = await state.get_data()

    product = await add_product(
        creator_tg_id=user.tg_id,
        name=data["name"],
        gender=data["gender"],
        category=data["category"],
        price=data["price"],
    )

    await state.clear()
    await message.answer(
        text=markdown.text(
            "✅ Одяг успішно доданий до каталогу.",
            f"Ось його унікальний ідентифікатор: {markdown.hcode(product.id)}.",
        ),
        reply_markup=build_root_keyboard(role=user.role),
    )


@router.message(AddProductSurvey.price, ~F.text.regexp(r"^[1-9][0-9]*$"))
async def add_product_survey_invalid_price_handler(message: Message) -> None:
    await message.answer(text="⚠️ Ціна може складатися лише з цифр. Введіть значення ще раз:")
