from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    year: int
    author_id: int


class AuthorCreateSchema(BaseModel):
    name: str


class BookResponseSchema(BaseModel):
    id: int
    title: str
    year: int
    author_id: int


class AuthorResponseSchema(AuthorCreateSchema):
    id: int
    books: list[BookResponseSchema] = []  # Список книг у автора


class UpdateBookSchema(BaseModel):
    title: str | None = None
    author_id: int | None = None
    year: int | None = None
