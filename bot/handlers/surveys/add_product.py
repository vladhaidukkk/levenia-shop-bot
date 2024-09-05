from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from bot.filters import ManagerFilter
from bot.keyboards.root import RootKeyboardText

router = Router(name=__name__)
router.message.filter(ManagerFilter())


class AddProductSurvey(StatesGroup):
    pass


@router.message(F.text == RootKeyboardText.ADD_PRODUCT)
async def add_product_button_handler(message: Message, state: FSMContext) -> None:
    pass
