from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    author: str
    year: int


class BookResponseSchema(BookCreateSchema):
    id: int
