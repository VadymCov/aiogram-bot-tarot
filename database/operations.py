from sqlalchemy import select
from database.database import SessionLocal
from database.models import User


async def get_or_create_user(telegram_id: int) -> User:
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


async def update_user(telegram_id: int, **kwargs):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            for field, value in kwargs.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            await session.commit()
            return user
        else:
            return None

