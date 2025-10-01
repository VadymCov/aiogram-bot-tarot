from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.inline import get_language_keyboard, get_main_keyboard
from database.operations import get_or_create_user
import json

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    user = await get_or_create_user(message.from_user.id)  # type: ignore
    user_name = message.from_user.first_name  # type: ignore
    # if not user.language:
    text = texts["menu"][user.language]["choose_language"].replace("{name}", user_name)
    await message.answer(text=text, reply_markup=get_language_keyboard(), parse_mode="HTML")
    # else:
    #     await message.answer(  # type: ignore
    #         text=texts["menu"][user.language]["main_menu_title"].replace("{name}", user_name),
    #         reply_markup=get_main_keyboard(user.language),
    #         parse_mode="HTML",
    #     )
