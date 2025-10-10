import asyncio
import logging
from aiogram import F, Bot, Dispatcher

from setup import preload_card, setup_dispatcher

from config.settings import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    try:
        bot = Bot(token=BOT_TOKEN)  # type: ignore
        dp = Dispatcher()
        logging.info("✅ Bot and dispatcher create")
    except Exception as e:
        logging.exception("❌ Failed to create bot")
        raise

    await preload_card()
    await setup_dispatcher(dp)

    logger.info("✅ The bot is starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("The Bot has been stopped ⛔")