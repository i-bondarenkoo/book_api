from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import ForeignKey


class BookOrm(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    author = relationship("AuthorOrm", back_populates="books")


class AuthorOrm(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    # back_populates показывает, что таблица authors имеет много книг (one-to-many)
    books: Mapped[list[BookOrm]] = relationship(
        "BookOrm", back_populates="author", cascade="all, delete-orphan"
    )
