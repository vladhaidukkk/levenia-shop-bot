import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.config import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer(text=markdown.text("👋", markdown.hbold(message.from_user.full_name)))


async def main() -> None:
    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
