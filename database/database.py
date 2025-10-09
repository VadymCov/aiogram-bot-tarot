from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base
from config.settings import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ❗❗❗ RESET DATABASE
async def reset_db_once():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
