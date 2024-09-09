from collections import defaultdict

from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils import markdown

from bot.db.queries.product import get_all_product_brands, get_all_product_categories, get_all_product_materials
from bot.filters.role import ManagerFilter
from bot.keyboards.reply.root import RootKeyboardText

router = Router(name=__name__)
router.message.filter(ManagerFilter())


def group_by_starting_letter(strings: list[str]) -> dict[str, list[str]]:
    letter_to_strings = defaultdict(list)
    for string in strings:
        if string:
            starting_letter = string[0].lower()
            letter_to_strings[starting_letter].append(string)
    return letter_to_strings


def format_grouped_strings(grouped_strings: dict[str, list[str]]) -> str:
    return markdown.text(
        *[
            markdown.text(markdown.hbold(f"{title.upper()}:"), ", ".join(string.title() for string in strings))
            for title, strings in grouped_strings.items()
        ],
        sep="\n",
    )


@router.message(F.text == RootKeyboardText.LIST_CATEGORIES)
async def list_categories_button_handler(message: Message) -> None:
    categories = await get_all_product_categories()
    grouped_categories = group_by_starting_letter(categories)
    await message.answer(format_grouped_strings(grouped_categories))


@router.message(F.text == RootKeyboardText.LIST_BRANDS)
async def list_brands_button_handler(message: Message) -> None:
    brands = await get_all_product_brands()
    grouped_brands = group_by_starting_letter(brands)
    await message.answer(format_grouped_strings(grouped_brands))


@router.message(F.text == RootKeyboardText.LIST_MATERIALS)
async def list_materials_button_handler(message: Message) -> None:
    materials = await get_all_product_materials()
    grouped_materials = group_by_starting_letter(materials)
    await message.answer(format_grouped_strings(grouped_materials))
