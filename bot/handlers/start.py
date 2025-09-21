from aiogram import Router, types
from aiogram.filters import Command

from languages import get_text

router = Router()

@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(get_text("welcome", )
    )
    pass