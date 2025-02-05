from fastapi import APIRouter
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_session_db
from schemas import BookCreateSchema


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


# @router.get("/search/{title}")
# async def search_book(title: str, session: AsyncSession = Depends(get_session_db)):
#     return await crud.search_book_db(title=title, session=session)


# @router.get("/filter/{year_left}/{year_right}")
# async def filter_book_for_year(
#     year_left: int, year_right: int, session: AsyncSession = Depends(get_session_db)
# ):
#     return await crud.filter_book_for_year_db(
#         year_left=year_left, year_right=year_right, session=session
#     )


# @router.get("/{author}")
# async def get_books_by_author(
#     author: str, session: AsyncSession = Depends(get_session_db)
# ):
#     return await crud.get_books_by_author_db(author=author, session=session)
