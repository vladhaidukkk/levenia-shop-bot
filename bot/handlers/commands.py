from re import Match

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.models import BonusType, BonusUnit, UserModel
from bot.db.queries.bonus import add_bonus
from bot.db.queries.referral import add_referral
from bot.db.queries.user import add_user, get_user
from bot.keyboards.root import build_root_keyboard

router = Router(name=__name__)


@router.message(
    CommandStart(
        deep_link=True,
        deep_link_encoded=True,
        magic=F.args.regexp(r"^referrer_id:(\d+)$").as_("referral"),
    )
)
async def referral_start_command_handler(message: Message, referral: Match[str], user: UserModel | None) -> None:
    referrer_tg_id = int(referral.group(1))
    referrer = await get_user(tg_id=referrer_tg_id)
    is_referral_applicable = bool(referrer and not user)

    if not user:
        user = await add_user(tg_id=message.from_user.id)

    if is_referral_applicable:
        bonus = await add_bonus(user_tg_id=referrer.tg_id, type_=BonusType.DISCOUNT, value=5, unit=BonusUnit.PERCENTAGE)
        await add_referral(user_tg_id=user.tg_id, referrer_tg_id=referrer.tg_id, bonus_id=bonus.id)

    await message.answer(
        # TODO: update welcome message
        text=markdown.text("👋", markdown.hbold(message.from_user.full_name)),
        reply_markup=build_root_keyboard(role=user.role),
    )


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
