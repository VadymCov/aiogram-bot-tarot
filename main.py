import asyncio 
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import BOT_TOKEN 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handlers(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!\n How are yoy")


async def main():
    logger.info("The bot is starting")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())