import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import callback_query
from aiogram_calendar import DialogCalendarCallback, SimpleCalendarCallback, DialogCalendar
from database.operations import update_user

from bot.keyboards import inline

import json

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

router = Router()

logger = logging.getLogger(__name__)


class UserStates(StatesGroup):
    waiting_for_birth_date = State()


@router.callback_query(F.data.startswith("lang_"))
async def language_handler(callback: types.CallbackQuery):
    # await get_or_create_user(callback.from_user.id)
    lang = callback.data.split("_")[1]  # type: ignore
    await update_user(callback.from_user.id, language=lang) # type: ignore
    logger.info(f"✅User {callback.from_user.first_name} chose the language: {lang}")
    # user = await get_or_create_user(callback.from_user.id)
    # lang = user.language

    await callback.answer(text=texts["menu"][lang]["language_changed"])
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["ask_gender"],
        reply_markup=inline.get_gender_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("gender_"))
async def gender_selection_handler(callback: types.CallbackQuery, lang: str):
    gender = callback.data.split("_")[1]  # type: ignore
    # user = await update_user(callback.from_user.id, gender=gender)
    user_name = callback.from_user.first_name
    logger.info(f"✅User {user_name} chose the gender: {gender}")
    await callback.answer(text=texts["menu"][lang]["saved"])
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["choose_birth_date"][1].replace("{name}", user_name),
        reply_markup=inline.get_calendar_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "set_birth_date")
async def birth_date_calendar_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    calendar = DialogCalendar(locale=lang)
    markup = await calendar.start_calendar()
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(text=texts["menu"][lang]["choose_birth_date"][0], reply_markup=markup)  # type: ignore


@router.callback_query(DialogCalendarCallback.filter(), UserStates.waiting_for_birth_date)
async def birth_data_save(
    callback: types.CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext, lang: str
):
    user_name = callback.from_user.first_name
    calendar = DialogCalendar(locale=lang)
    selected, date_selected = await calendar.process_selection(callback, callback_data) # type: ignore
    if selected:
        await update_user(callback.from_user.id, birth_date=date_selected)
        await state.clear()
        await callback.answer(text=texts["menu"][lang]["saved"])
        await callback.message.edit_text(  # type: ignore
            text=texts["menu"][lang]["main_menu_title"].replace("{name}", user_name), reply_markup=inline.get_main_keyboard(lang), parse_mode="HTML"
        )
