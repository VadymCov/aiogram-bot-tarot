import asyncio 
import logging
from aiogram import Bot, Dispatcher


from database.database import init_db
from bot.handlers.start import router as start_router
from bot.handlers.callbacks import router as callback_router
from config.settings import BOT_TOKEN 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def main():
    try:
        await init_db()
        logging.info("✅ The database has been initialized")
    except Exception as e:
        logging.info("❌ Failed to initialize database")
        raise Exception(f"{e}")


    try:
        bot = Bot(token=BOT_TOKEN) # type: ignore
        dp = Dispatcher()
        logging.info("✅ Bot and dispatcher create")
    except Exception as e:
        logging.info("❌ Failed to create bot")
        raise Exception(f"{e}")

    try:
        dp.include_router(start_router)
        dp.include_router(callback_router)
        logging.info("✅ All handlers registered")
    except Exception as e:
        logging.info("❌ Failed to register handlers: {e}")
        return

    logger.info("✅ The bot is starting")   
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())