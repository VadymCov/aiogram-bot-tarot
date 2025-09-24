import asyncio 
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from database.database import engine
from database.models import Base

from config.settings import BOT_TOKEN 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("The database has been initialized✅")
    except Exception as e:
        logging.info("Failed to initialize database📛")
        raise Exception(f"{e}")

@dp.message(Command("start"))
async def start_handlers(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!\n How are yoy")


async def main():

    await init_db()

    logger.info("The bot is starting✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())