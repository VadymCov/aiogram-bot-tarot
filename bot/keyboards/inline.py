from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json

with open("data/text_inline.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ua"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton(text="🌐 Русский", callback_data="lang_ru"),
            ]
        ]
    )


def get_gender_keyboard(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts["buttons"][lang]["gender_male"],
                    callback_data="gender_male",
                ),
                InlineKeyboardButton(
                    text=texts["buttons"][lang]["gender_female"],
                    callback_data="gender_female",
                ),
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["choose_later"], callback_data="set_birth_date"),
            ],
        ]
    )


def get_calendar_keyboard(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["choose_birth_date"], callback_data="set_birth_date"),
                InlineKeyboardButton(text=texts["buttons"][lang]["choose_later"], callback_data="main_menu"),
            ]
        ]
    )


def get_main_keyboard(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["card_of_day"], callback_data="vadaram_card"),
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["family_advice"], callback_data="family_advice"),
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["obusha"], callback_data="obusha_card")
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["settings"], callback_data="setting"),
            ],
        ]
    )


def get_return_to_edit_menu(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["back_to_menu"], callback_data="edit_menu")
            ]
        ]
    )


def get_return_to_menu(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["back_to_menu"], callback_data="main_menu")
            ]
        ]
    )


# ⚙️
def get_settings_keyboard(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["change_language"], callback_data="change_lang"),
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["change_gender"], callback_data="change_gender"),
            ],
            [
                InlineKeyboardButton(text=texts["buttons"][lang]["change_birth_date"], callback_data="set_birth_date"),
            ],
            [InlineKeyboardButton(text=texts["buttons"][lang]["back_to_menu"], callback_data="edit_menu")],
        ]
    )


# ⚙️
def get_settings_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇦 Українська", callback_data="save_ua"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="save_en"),
                InlineKeyboardButton(text="🌐 Русский", callback_data="save_ru"),
            ]
        ]
    )


# ⚙️
def get_setting_gender_keyboard(lang="en"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts["buttons"][lang]["gender_male"],
                    callback_data="save_male",
                ),
                InlineKeyboardButton(
                    text=texts["buttons"][lang]["gender_female"],
                    callback_data="save_female",
                ),
            ],
        ]
    )
