from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, DateTime, Date, func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    language: Mapped[str] = mapped_column(String(3), default="ru")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    gender: Mapped[str] = mapped_column(String(10), nullable=True, default=None)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True, default=None)
    last_card_date: Mapped[Date] = mapped_column(Date, nullable=True)
