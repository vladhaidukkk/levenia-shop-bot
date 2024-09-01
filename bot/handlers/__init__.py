from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(text=markdown.text("👋", markdown.hbold(message.from_user.full_name)))
