from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_calendar import DialogCalendarCallback, SimpleCalendarCallback, DialogCalendar
from services.user_service import UserService

from bot.keyboards import inline
import json


router = Router()

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


class UserStates(StatesGroup):
    waiting_for_birth_date = State()


@router.callback_query(F.data.startswith("lang_"))
async def language_save_handler(callback: types.CallbackQuery, lang: str):
    lang = callback.data.split("_")[1]  # type: ignore
    await UserService.update_user_field(callback.from_user.id, field=lang)
    await callback.answer(text=texts["menu"][lang]["language_changed"])
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["ask_gender"],
        reply_markup=inline.get_gender_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "change_lang")  # ⚙️
async def settings_language_handler(callback: types.CallbackQuery, lang: str):
    await callback.message.edit_text(  # type:ignore
        text=texts["menu"][lang]["choose_language"].split("\n")[1] + " 🌐",
        reply_markup=inline.get_settings_language_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("gender_"))
async def gender_selection_handler(callback: types.CallbackQuery, lang: str):
    gender = callback.data.split("_")[1]  # type: ignore
    await UserService.update_user_field(callback.from_user.id, field=gender)
    user_name = callback.from_user.first_name
    await callback.answer(text=texts["menu"][lang]["saved"])
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["choose_birth_date"][1].replace("{name}", user_name),
        reply_markup=inline.get_calendar_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "change_gender")  # ⚙️
async def settings_gender_handler(callback: types.CallbackQuery, lang: str):
    await callback.message.edit_text(  # type:ignore
        text=texts["menu"][lang]["ask_gender"], reply_markup=inline.get_setting_gender_keyboard(lang), parse_mode="HTML"
    )


@router.callback_query(F.data == "set_birth_date")
async def birth_date_calendar_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    await state.update_data(return_to="main_menu")
    calendar = DialogCalendar(locale=lang)
    markup = await calendar.start_calendar(year=1990)
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["choose_birth_date"][0], reply_markup=markup
    )


@router.callback_query(F.data == "set_birth_date")  # ⚙️
async def settings_birth_date_calendar_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    await state.update_data(retutn_tu="settings")
    calendar = DialogCalendar(locale=lang)
    markup = await calendar.start_calendar(year=1990)
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["choose_birth_date"][0], reply_markup=markup
    )


@router.callback_query(DialogCalendarCallback.filter(), UserStates.waiting_for_birth_date)
async def birth_data_save_handler(
    callback: types.CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext, lang: str
):
    user_name = callback.from_user.first_name
    calendar = DialogCalendar(locale=lang)
    selected, date_selected = await calendar.process_selection(callback, callback_data)  # type: ignore
    if selected:
        await UserService.update_user_field(callback.from_user.id, field=date_selected)
        state_data = await state.get_data()
        return_to = state_data.get("return_to", "main_menu")
        if return_to == "main_menu":
            await callback.message.edit_text(  # type: ignore
                text=texts["menu"][lang]["main_menu_title"].replace("{name}", user_name),
                reply_markup=inline.get_main_keyboard(lang),
                parse_mode="HTML",
            )
        else:
            await callback.message.edit_text(  # type: ignore
                await callback.message.edit_text(  # type: ignore
                    text=texts["menu"][lang]["title"], reply_markup=inline.get_settings_keyboard(lang), parse_mode="HTML"
                )
            )
        await state.clear()
        await callback.answer(text=texts["menu"][lang]["saved"])


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: types.CallbackQuery, lang: str):
    user_name = callback.from_user.first_name
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["main_menu_title"].replace("{name}", user_name),
        reply_markup=inline.get_main_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "setting")
async def user_settings(callback: types.CallbackQuery, lang: str):
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["title"], reply_markup=inline.get_settings_keyboard(lang), parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("save_"))
async def save_settings_handler(callback: types.CallbackQuery, lang: str):
    field = callback.data.split("_")[1]  # type: ignore
    user_name = callback.from_user.first_name
    await UserService.update_user_field(callback.from_user.id, field=field)
    await callback.answer(text=texts["menu"][lang]["saved"])
    await callback.message.edit_text(  # type: ignore
        text=texts["menu"][lang]["main_menu_title"].replace("{name}", user_name),
        reply_markup=inline.get_main_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "in_dev")
async def in_development_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer(text=texts["menu"][lang]["in_development"])
