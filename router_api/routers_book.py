from fastapi import APIRouter
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_session_db
from schemas import BookCreateSchema, UpdateBookSchema


router = APIRouter()


@router.post("/")
async def create_book(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    return await crud.create_book_db(
        book=book,
        session=session,
    )


@router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session_db)):
    return await crud.get_all_books_db(session=session)


@router.get("/{book_id}")
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session_db)):
    return await crud.get_book_by_id_db(book_id=book_id, session=session)


@router.delete("/{book_id}")
async def delete_book(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    return await crud.delete_book_db(book_id=book_id, session=session)


@router.patch("/{book_id}")
async def update_book(
    update_book: UpdateBookSchema,  # Модель для обновления
    book_id: int,
    session: AsyncSession = Depends(get_session_db),
):
    return await crud.update_book_db(
        update_book=update_book, book_id=book_id, session=session
    )
