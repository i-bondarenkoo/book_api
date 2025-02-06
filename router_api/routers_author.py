from fastapi import APIRouter
from fastapi import APIRouter
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_session_db
from schemas import AuthorCreateSchema, AuthorResponseSchema

router = APIRouter()


@router.post("/")
async def create_autor(
    author: AuthorCreateSchema, session: AsyncSession = Depends(get_session_db)
):
    await crud.create_author_db(author=author, session=session)


@router.get("/")
async def get_all_authors(session: AsyncSession = Depends(get_session_db)):
    return await crud.get_all_authors_db(session=session)


@router.get("/{author_id}")
async def get_author_by_id(
    author_id: int, session: AsyncSession = Depends(get_session_db)
):
    return await crud.get_author_by_id_db(author_id=author_id, session=session)


@router.delete("/{author_id}")
async def delete_author(
    author_id: int, session: AsyncSession = Depends(get_session_db)
):
    return await crud.delete_author_db(author_id=author_id, session=session)


@router.put("/{author_id}")
async def update_author(
    name: str, author_id: int, session: AsyncSession = Depends(get_session_db)
):
    await crud.update_author_db(name=name, author_id=author_id, session=session)
