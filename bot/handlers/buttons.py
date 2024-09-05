from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.utils.deep_linking import create_start_link

from bot.keyboards.root import RootKeyboardText

router = Router(name=__name__)


@router.message(F.text == RootKeyboardText.INVITE_FRIEND)
async def invite_friend_button_handler(message: Message) -> None:
    ref_link = await create_start_link(bot=message.bot, payload=f"referrer_id:{message.from_user.id}", encode=True)
    await message.answer(
        markdown.text(
            "📤 Поділіться цим посиланням з другом:",
            markdown.hcode(ref_link),
            "і отримайте 5% знижки на наступну покупку.",
            sep="\n",
        )
    )
