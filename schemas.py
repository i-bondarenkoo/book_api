from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    author: str
    year: int


class BookResponseSchema(BookCreateSchema):
    id: int


class UpdateBookSchema(BookCreateSchema):
    title: str | None = None
    author: str | None = None
    year: int | None = None
