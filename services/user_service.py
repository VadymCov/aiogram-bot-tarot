from database.operations import update_user
import logging


logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    async def set_language(user_id: int, lang: str):
        await update_user(user_id, language=lang)
        logger.info(f"✅User {user_id} chose the language: {lang}")

    @staticmethod
    async def set_gender(user_id: int, gender: str):
        await update_user(user_id, gender=gender)
        logger.info(f"✅ User {user_id} choose the gender: {gender}")

    @staticmethod
    async def set_birth_date(user_id: int, date_selected: str):
        await update_user(user_id, birth_date=date_selected)
        logger.info(f"✅ User {user_id} choose the birth date: {date_selected}")
