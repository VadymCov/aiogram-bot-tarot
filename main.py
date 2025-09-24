import asyncio 
import logging
from aiogram import Bot, Dispatcher, types


from database.database import engine
from database.models import Base
from bot.handlers.start import router as start_router

from config.settings import BOT_TOKEN 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("✅ The database has been initialized")
    except Exception as e:
        logging.info("❌ Failed to initialize database")
        raise Exception(f"{e}")

async def main():
    await init_db()

    try:
        bot = Bot(token=BOT_TOKEN) # type: ignore
        dp = Dispatcher()
        logging.info("✅ Bot and dispatcher create")
    except Exception as e:
        logging.info("❌ Failed to create bot")
        raise Exception(f"{e}")

    try:
        dp.include_router(start_router)
        logging.info("✅ All handlers registered")
    except Exception as e:
        logging.info("❌ Failed to register handlers: {e}")
        return

    logger.info("✅ The bot is starting")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())