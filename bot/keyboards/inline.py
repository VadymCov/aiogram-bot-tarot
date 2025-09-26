from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json
with open("data/text_inline.json", "r", encoding="utf-8") as f:
    texts = json.load(f)


def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="ua Українська", callback_data="lang_ua"),
            InlineKeyboardButton(text="us English", callback_data="lang_en"),
            InlineKeyboardButton(text="ru Русский", callback_data="lang_ru")
        ]
    ])

def get_gender_keyboard(lang="en"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=texts["buttons"][lang]["gender_male"], callback_data="qw"),
            InlineKeyboardButton(text=texts["buttons"][lang]["gender_female"], callback_data="qw"),
            InlineKeyboardButton(text=texts["buttons"][lang]["choose_later"], callback_data="qw"),


        ]
    ])

def get_main_keyboard(lang="en"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=texts["buttons"][lang]["card_of_day"], callback_data="qw"),
            InlineKeyboardButton(text=texts["buttons"][lang]["rune_spread"], callback_data="qw")

        ],

        [
            InlineKeyboardButton(text=texts["buttons"][lang]["moon_calendar"], callback_data="qw"),
            InlineKeyboardButton(text=texts["buttons"][lang]["meditation"], callback_data="qw")
        ],

        [
            InlineKeyboardButton(text=texts["buttons"][lang]["family_advice"], callback_data="qw"),
            InlineKeyboardButton(text=texts["buttons"][lang]["guardian_angel"], callback_data="qw")
        ],

        [
            InlineKeyboardButton(text=texts["buttons"][lang]["settings"], callback_data="qw"),
        ]
    ])