from schemas import BookCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from database import get_session_db
from sqlalchemy import select
from models import BookOrm


async def create_book(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    new_book = BookOrm(**book.model_dump())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


async def get_all_books(session: AsyncSession = Depends(get_session_db)):
    stmt = select(BookOrm).order_by(BookOrm.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_book_by_id(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> BookOrm | None:
    stmt = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return result.scalars().first()


async def delete_book(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    result = await get_book_by_id(book_id, session)
    await session.delete(result)
    await session.commit()
