from fastapi import APIRouter
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_session_db
from models import BookOrm


router = APIRouter()


@router.post("/")
async def create_book(book: BookOrm, session: AsyncSession = Depends(get_session_db)):
    return await crud.create_book(
        book=book,
        session=session,
    )


@router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session_db)):
    return await crud.get_all_books(session=session)


@router.get("/{book_id}")
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session_db)):
    return await crud.get_book_by_id(book_id=book_id, session=session)


@router.delete("/{book_id}")
async def delete_book(
    book_id: int, session: AsyncSession = Depends(get_session_db)
) -> None:
    return await crud.delete_book(book_id=book_id, session=session)
