from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.models import UserModel
from bot.db.queries.user import add_user
from bot.keyboards.root import build_root_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message, user: UserModel | None) -> None:
    if not user:
        user = await add_user(tg_id=message.from_user.id)
    await message.answer(
        # TODO: update welcome message
        text=markdown.text("👋", markdown.hbold(message.from_user.full_name)),
        reply_markup=build_root_keyboard(role=user.role),
    )


@router.message(Command("id"))
async def id_command_handler(message: Message) -> None:
    await message.answer(text=markdown.hcode(message.from_user.id))
