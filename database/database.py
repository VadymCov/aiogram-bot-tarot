from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/astro_bot"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)