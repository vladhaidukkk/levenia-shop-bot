import contextlib

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.queries.user import add_user
from bot.errors import UserAlreadyExistsError

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    with contextlib.suppress(UserAlreadyExistsError):
        await add_user(tg_id=message.from_user.id)
    await message.answer(text=markdown.text("👋", markdown.hbold(message.from_user.full_name)))


@router.message(Command("id"))
async def id_command_handler(message: Message) -> None:
    await message.answer(text=markdown.hcode(message.from_user.id))
