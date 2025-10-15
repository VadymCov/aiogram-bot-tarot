from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram_calendar import DialogCalendarCallback, DialogCalendar

from bot.handlers.callbacks import UserStates
from bot.keyboards import inline
from services.user_service import UserService

import json

with (open("data/text_menu.json", "r", encoding="UTF-8") as f,
      open("data/text_inline.json", "r", encoding="UTF-8") as f_b):
    texts = json.load(f)
    texts_button = json.load(f_b)

router: Router = Router()


@router.callback_query(F.data == "set_birth_date")
async def birth_date_calendar_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    await state.update_data(return_to="main_menu")
    cancel_text = texts_button["buttons"][lang]["choose_later"]
    calendar = DialogCalendar(locale=lang, cancel_btn=cancel_text)
    markup = await calendar.start_calendar(year=1990)
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(text=texts["menu"][lang]["choose_birth_date"], reply_markup=markup)  # type: ignore


@router.callback_query(F.data == "set_birth_date")  # ⚙️
async def settings_birth_date_calendar_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    await state.update_data(return_tu="settings")
    cancel_text = texts_button["buttons"][lang]["choose_later"]
    calendar = DialogCalendar(locale=lang, cancel_btn=cancel_text)
    calendar = DialogCalendar(locale=lang)
    markup = await calendar.start_calendar(year=1990)
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(text=texts["menu"][lang]["choose_birth_date"], reply_markup=markup)  # type: ignore


@router.callback_query(DialogCalendarCallback.filter(), UserStates.waiting_for_birth_date)
async def birth_data_save_handler(
        callback: types.CallbackQuery, callback_data: DialogCalendarCallback, state: FSMContext, lang: str
):
    if callback.data is not None and "CANCEL" in callback.data:
        await state.clear()
        await callback.message.edit_text(  # type: ignore
            text=texts["menu"][lang]["main_menu_title"], reply_markup=inline.get_main_keyboard(lang)
        )
        return None

    cancel_text = texts_button["buttons"][lang]["choose_later"]
    calendar = DialogCalendar(locale=lang, cancel_btn=cancel_text)
    selected, date_selected = await calendar.process_selection(callback, callback_data)  # type: ignore

    if selected:
        if date_selected.year < 1940 or date_selected.year > 2015:
            await callback.answer(texts["menu"][lang]["errors"], show_alert=True)
            return None

        await UserService.update_user_field(callback.from_user.id, birth_data=date_selected)
        state_data = await state.get_data()
        return_to = state_data.get("return_to", "main_menu")

        if return_to == "main_menu":
            await callback.message.edit_text(  # type: ignore
                text=texts["menu"][lang]["main_menu_title"],
                reply_markup=inline.get_main_keyboard(lang),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(  # type: ignore
                text=texts["menu"][lang]["title"],
                reply_markup=inline.get_settings_keyboard(lang),
                parse_mode="HTML"
            )

        await state.clear()
        await callback.answer(text=texts["menu"][lang]["saved"])

    return None
