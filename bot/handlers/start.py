from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.inline import get_language_keyboard
from database.operations import get_or_create_user
import json

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = await get_or_create_user(message.from_user.id)  # type: ignore
    user_name = message.from_user.first_name  # type: ignore
    text = texts["menu"][user.language]["choose_language"].replace("{name}", user_name)
    await message.answer(
        text=text, reply_markup=get_language_keyboard(), parse_mode="HTML"
    )
