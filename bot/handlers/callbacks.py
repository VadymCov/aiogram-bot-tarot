from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_calendar import DialogCalendar
from services.user_service import UserService
from utils.locale_helper import get_system_locale
from bot.keyboards import inline
import json

router: Router = Router()

with open("data/text_menu.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


class UserStates(StatesGroup):
    waiting_for_birth_date = State()


@router.callback_query(F.data.startswith("lang_"))
async def language_save_handler(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]  
    await UserService.update_user_field(callback.from_user.id, language=lang)
    await callback.answer(text=texts["menu"][lang]["language_changed"])
    await callback.message.edit_text(  
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
async def gender_selection_handler(callback: types.CallbackQuery, state: FSMContext, lang: str):
    gender = callback.data.split("_")[1]  
    await UserService.update_user_field(callback.from_user.id, gender=gender)
    await callback.answer(text=texts["menu"][lang]["saved"])

    await state.update_data(return_to="main_menu")
    system_locale = get_system_locale(lang)
    cancel_text = "⏩ choose_later"
    calendar = DialogCalendar(locale=system_locale, cancel_btn=cancel_text)
    markup = await calendar.start_calendar(year=1990)
    await state.set_state(UserStates.waiting_for_birth_date)
    await callback.message.edit_text(
        text=texts["menu"]["en"]["choose_birth_date"],
        reply_markup=markup,
    )


@router.callback_query(F.data == "change_gender")  # ⚙️
async def settings_gender_handler(callback: types.CallbackQuery, lang: str):
    await callback.message.edit_text(  # type:ignore
        text=texts["menu"][lang]["ask_gender"], reply_markup=inline.get_setting_gender_keyboard(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "main_menu")
async def return_to_main_menu_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=texts["menu"][lang]["main_menu_title"],
        reply_markup=inline.get_main_keyboard(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "setting")
async def user_settings(callback: types.CallbackQuery, lang: str):
    await callback.message.edit_text(
        text=texts["menu"][lang]["title"], reply_markup=inline.get_settings_keyboard(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("save_"))
async def save_settings_handler(callback: types.CallbackQuery, lang: str):
    field = callback.data.split("_")[1]  
    if field in ["ua", "en", "ru"]:
        await UserService.update_user_field(callback.from_user.id, language=field)
        await callback.answer(text=texts["menu"][lang]["saved"])
        await callback.message.edit_text(
            text=texts["menu"][field]["main_menu_title"],
            reply_markup=inline.get_main_keyboard(field),
            parse_mode="HTML"
        )
        return

    elif field in ["male", "female"]:
        await UserService.update_user_field(callback.from_user.id, gender=field)
    else:
        await UserService.update_user_field(callback.from_user.id, birth_date=field)
    await callback.answer(text=texts["menu"][lang]["saved"])
    await callback.message.edit_text(
        text=texts["menu"][lang]["main_menu_title"], reply_markup=inline.get_main_keyboard(lang),
        parse_mode="HTML"
    )
    return


@router.callback_query(F.data == "in_dev")
async def in_development_handler(callback: types.CallbackQuery, lang: str):
    await callback.answer(text=texts["menu"][lang]["in_development"])


