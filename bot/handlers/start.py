from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.inline import get_language_keyboard
from database.operations import get_or_create_user

from bot.locales.utils import get_text

router = Router()

@router.message(Command('start'))
async def start_handler(message: types.Message):
    user =  await get_or_create_user(message.from_user.id) # type: ignore
    await message.answer(get_text("welcome", user.language),
        reply_markup=get_language_keyboard()
        )