from schemas import BookCreateSchema, BookResponseSchema, UpdateBookSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from database import get_session_db
from sqlalchemy import select, func
from models import BookOrm


async def create_book_db(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    new_book = BookOrm(**book.model_dump())  # Pydantic → ORM
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


async def get_all_books_db(session: AsyncSession = Depends(get_session_db)):
    stmt = select(BookOrm).order_by(BookOrm.id)
    # Когда ты выполняешь session.execute(stmt), SQLAlchemy возвращает объект с результатами (Result),
    # но не сами объекты BookOrm.
    # scalars() извлекает только объекты BookOrm, а не сырые строки SQL.
    # 📌 Без .scalars() ты бы получил что-то вроде списка кортежей, а не нормальный список объектов.
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_book_by_id_db(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> BookOrm | None:
    stmt = select(BookOrm).where(BookOrm.id == book_id)
    result = await session.execute(stmt)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


async def delete_book_db(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    result = await get_book_by_id_db(book_id, session)
    await session.delete(result)
    await session.commit()


# async def search_book_db(title: str, session: AsyncSession = Depends(get_session_db)):
#     # Убираем лишние пробелы и приводим к нижнему регистру
#     title = title.strip().lower()

#     # Формируем SQL-запрос с приведением к нижнему регистру в SQL
#     stmt = select(BookOrm).where(
#         func.lower(func.trim(BookOrm.title)).like(f"%{title}%")
#     )

#     print(f"Ищем: {repr(title)}")

#     # Выводим запрос в консоль для отладки
#     print(f"SQL-запрос: {stmt}")

#     # Выполняем запрос
#     result = await session.execute(stmt)
#     book_search = result.scalars().all()

#     # Если книг нет, выбрасываем 404 ошибку
#     if not book_search:
#         raise HTTPException(status_code=404, detail="Книга не найдена")

#     # Преобразуем ORM-объекты в Pydantic-модели перед возвратом
#     return [BookResponseSchema.model_validate(book) for book in book_search]


# async def filter_book_for_year_db(
#     year_left: int, year_right: int, session: AsyncSession = Depends(get_session_db)
# ):
#     if year_left > year_right:
#         raise ValueError("Левая граница должна быть меньше правой")
#     stmt = select(BookOrm).where(
#         (BookOrm.year >= year_left) & (BookOrm.year <= year_right)
#     )
#     # stmt = select(BookOrm).where(BookOrm.year.between(year_left, year_right))
#     result = await session.execute(stmt)
#     book_search = result.scalars().all()
#     if not book_search:
#         raise HTTPException(
#             status_code=404, detail="Книги с указанным диапазоном не найдены"
#         )
#     return [BookResponseSchema.model_validate(book) for book in book_search]


# # async def update_book_db(book: UpdateBookSchema, session: AsyncSession = Depends(get_session_db)):
# #     update_book = BookOrm(**book.model_dump())
# #     result = await session.


# async def get_books_by_author_db(
#     author: str, session: AsyncSession = Depends(get_session_db)
# ):
#     author = author.lower().strip()
#     stmt = select(BookOrm).where(func.lower(BookOrm.title).strim() == author)
#     result = await session.execute(stmt)
#     book_search = result.scalars().all()
#     if not book_search:
#         raise HTTPException(status_code=404, detail="Книги этого автора не найдены")
#     return book_search
