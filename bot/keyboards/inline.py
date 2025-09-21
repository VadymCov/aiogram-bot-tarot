from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ua Українська", callback_data="lang_uk")],
        [InlineKeyboardButton(text="ru Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="us English", callback_data="lang_en")]
    ])
