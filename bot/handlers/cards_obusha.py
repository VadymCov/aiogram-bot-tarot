from aiogram import F, Router, types, exceptions

import json
import logging
from random import randint
from datetime import date

from bot.keyboards import inline

from database.operations import get_or_create_user
from services.user_service import UserService
from services.card_service import CardService

router: Router = Router()
logger = logging.getLogger(__name__)

with open("data/text_menu.json", "r", encoding="UTF-8") as f:
    texts = json.load(f)


@router.callback_query(F.data == "obusha_card")
async def obusha_deck_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer()

    num_card = str(randint(1, 78))
    deck_name = "obusha"
    user = await get_or_create_user(callback.from_user.id)

    if user.last_obusha_date == date.today():
        try:
            await callback.message.edit_text(
                text="\n".join(texts["menu"][lang]["card_one_day"]),
                reply_markup=inline.get_main_keyboard(lang),
                parse_mode="HTML"
            )
        except exceptions.TelegramBadRequest as e:
            if "message is not modified" in str(e):  # ✅ ПРАВИЛЬНО
                logger.debug(f"🪚User {callback.from_user.id} pressed the button again")
                return
            raise

    await UserService.update_user_field(callback.from_user.id, last_obusha_date=date.today())
    image_id = await CardService.get_media_id(deck_name, num_card)
    card_data = await CardService.get_card_descriptions(num_card, deck_name, lang)
    card_caption = f"<b>{card_data["name"]}</b>\n\n<i>{card_data["descriptions"]}</i>"
    media = types.InputMediaPhoto(media=image_id, caption=card_caption, parse_mode="HTML")

    await callback.message.edit_media(media=media,
                                      reply_markup=inline.get_return_tu_edit_menu(lang),
                                      protect_content=True)


@router.callback_query(F.data == "edit_menu")
async def edit_menu_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer()
    try:
        await callback.message.answer(
            text=texts["menu"][lang]["main_menu_title"],
            reply_markup=inline.get_main_keyboard(lang),
            parse_mode="HTML"
        )
    except exceptions.TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            logger.exception("❗Critical error when trying to replace media with text")
            raise
    await callback.message.delete()
    return
