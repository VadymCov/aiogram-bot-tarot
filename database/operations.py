from sqlalchemy import select
from database.database import SessionLocal
from database.models import User

async def get_or_create(telegram_id: int) -> User:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user

async def update_user_language(telegram_id: int, language: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user =result.scalar_one_or_none()

        if user:
            user.language = language
            await session.commit()