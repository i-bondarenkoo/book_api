from tkinter import Y
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends


# базовый класс от которого наследуют все модели
class Base(DeclarativeBase):
    pass


# движок, отвечает за подключение к базе
engine = create_async_engine("sqlite+aiosqlite:///database.db")

# фабрика сессий для асинхронной работы с базой
AsyncSession = async_sessionmaker(bind=engine)


# функция для получения сессии для работы с базой
async def get_session_db():
    async with AsyncSession() as session:
        yield session
