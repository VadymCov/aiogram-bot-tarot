from datetime import date
from random import randint

import aiogram
from aiogram import types, F, Router

from bot.keyboards import inline
from database.operations import get_or_create_user
from services.card_service import CardService
from services.user_service import UserService

import json

router: Router = Router()

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


@router.callback_query(F.data == "family_advice")
async def family_advice_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer()
    num_card = str(randint(1, 59))
    deck_name = "family_advice"
    user = await get_or_create_user(callback.from_user.id)
    try:
        if user.last_card_date == date.today():
            await callback.message.edit_text(
                text="\n".join(texts["menu"][lang]["card_one_day"]), reply_markup=inline.get_main_keyboard(lang),
                parse_mode="HTML"
            )
            return
    except aiogram.exceptions.TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise
    else:
        await UserService.update_user_field(callback.from_user.id, last_card_date=date.today())
        image_id = await CardService.get_media_id_by_lang(deck_name, num_card, lang)
        media = types.InputMediaPhoto(media=image_id)
        await callback.message.edit_media(media=media, reply_markup=inline.get_return_tu_menu(lang))
        return
