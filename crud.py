from schemas import BookCreateSchema, BookResponseSchema, UpdateBookSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from database import get_session_db
from sqlalchemy import select, update
from models import BookOrm, AuthorOrm
from schemas import AuthorCreateSchema, AuthorResponseSchema
from sqlalchemy.orm import selectinload


async def create_book_db(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    # Проверка наличия автора
    stmt = select(AuthorOrm).where(AuthorOrm.id == book.author_id)
    result = await session.execute(stmt)
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    # Создание новой книги с привязкой к автору
    new_book = BookOrm(**book.model_dump())  # Pydantic → ORM
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return BookResponseSchema.model_validate(new_book.__dict__)


async def get_all_books_db(session: AsyncSession = Depends(get_session_db)):
    stmt = select(BookOrm).order_by(BookOrm.id).options(selectinload(BookOrm.author))
    # Когда ты выполняешь session.execute(stmt), SQLAlchemy возвращает объект с результатами (Result),
    # но не сами объекты BookOrm.
    # scalars() извлекает только объекты BookOrm, а не сырые строки SQL.
    # 📌 Без .scalars() ты бы получил что-то вроде списка кортежей, а не нормальный список объектов.
    result = await session.execute(stmt)
    books = result.scalars().all()
    # Преобразуем каждый объект BookOrm в Pydantic модель
    return [BookResponseSchema.model_validate(book.__dict__) for book in books]


async def get_book_by_id_db(
    book_id: int, session: AsyncSession = Depends(get_session_db)
):
    stmt = (
        select(BookOrm)
        .where(BookOrm.id == book_id)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(stmt)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return BookResponseSchema.model_validate(book.__dict__)


async def delete_book_db(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    result = result = await session.get(BookOrm, book_id)
    await session.delete(result)
    await session.commit()


async def update_book_db(
    update_book: UpdateBookSchema,
    book_id: int,
    session: AsyncSession = Depends(get_session_db),
):
    stmt = (
        select(BookOrm)
        .where(BookOrm.id == book_id)
        .options(selectinload(BookOrm.author))
    )
    result = await session.execute(stmt)
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if update_book.title is not None:
        book.title = update_book.title
    if update_book.author_id is not None:
        book.author_id = update_book.author_id
    if update_book.year is not None:
        book.year = update_book.year

    await session.commit()
    await session.refresh(book)

    # Преобразуем ORM-объект в словарь с помощью __dict__
    return BookResponseSchema.model_validate(book.__dict__)


async def create_author_db(
    author: AuthorCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    new_author = AuthorOrm(**author.model_dump())  # Pydantic → ORM
    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
    return new_author


async def get_all_authors_db(session: AsyncSession = Depends(get_session_db)):
    stmt = (
        select(AuthorOrm).order_by(AuthorOrm.id).options(selectinload(AuthorOrm.books))
    )
    result = await session.execute(stmt)
    all_books = result.scalars().all()
    return all_books


async def get_author_by_id_db(
    author_id: int, session: AsyncSession = Depends(get_session_db)
):
    stmt = (
        select(AuthorOrm)
        .where(AuthorOrm.id == author_id)
        .options(selectinload(AuthorOrm.books))
    )
    result = await session.execute(stmt)
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author


async def delete_author_db(
    author_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    author = await session.get(AuthorOrm, author_id)
    if author:
        await session.delete(author)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail="Автор не найден")


# async def update_author_db(
#     name: str, author_id: int, session: AsyncSession = Depends(get_session_db)
# ):
#     author = update(AuthorOrm).where(AuthorOrm.id == author_id).values(name=name)
#     await session.execute(author)
#     await session.commit()
#     if author is None:
#         raise HTTPException(status_code=404, detail="Автор не найден")
#     return AuthorCreateSchema.model_validate(author.__dict__)


async def update_author_db(
    name: str, author_id: int, session: AsyncSession = Depends(get_session_db)
):
    # Выполняем обновление
    result = await session.execute(
        update(AuthorOrm).where(AuthorOrm.id == author_id).values(name=name)
    )
    await session.commit()

    # Проверяем, были ли обновлены записи
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Автор не найден")

    # Получаем обновленного автора
    updated_author = await session.get(AuthorOrm, author_id)

    # Если автор найден, возвращаем его через Pydantic модель
    if updated_author:
        return AuthorCreateSchema(name=updated_author.name)
    else:
        raise HTTPException(status_code=404, detail="Автор не найден")
