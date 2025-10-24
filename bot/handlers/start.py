import json
from datetime import date
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from bot.keyboards.inline import get_language_keyboard, get_main_keyboard
from database.operations import get_or_create_user
from utils.logger import AppLogging

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

with open("data/media_ids/birthday_ids.json", "r", encoding="utf-8") as f:
    birthday_ids = json.load(f)

logger = AppLogging.get_logger()
router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    user = await get_or_create_user(message.from_user.id)
    user_name = message.from_user.first_name
    today = date.today()

    if user.birth_date and isinstance(user.birth_date,
                                      date) and user.birth_date.month == today.month and user.birth_date.day == today.day:
        if "birthday" in birthday_ids:
            file_id = birthday_ids["birthday"]
            birthday_text = texts["menu"][user.language]["birthday_text"]

            try:
                await message.answer_photo(
                    photo=file_id,
                    caption=birthday_text,
                    parse_mode="HTML"
                )
                logger.info(f"🎉 Birthday picture sent to the user: {message.from_user.id}")
            except Exception as e:
                logger.error(f"❌ Error sending a picture: {e}")
                await message.answer(text=birthday_text, parse_mode="HTML")

    if user.language:
        await message.answer(
            text=texts["menu"]["ua"]["main_menu_title"].replace("{name}", user_name),
            reply_markup=get_main_keyboard(user.language),
            parse_mode="HTML",
        )
    else:
        text = texts["menu"]["ua"]["choose_language"].replace("{name}", user_name)
        await message.answer(text=text, reply_markup=get_language_keyboard(), parse_mode="HTML")

    try:
        await message.delete()
        logger.debug(f"🗑️ Delete /start command from user {message.from_user}")
    except TelegramBadRequest as e:
        logger.warning(f"⚠️ Could not delete /start command: {e}")
        pass
