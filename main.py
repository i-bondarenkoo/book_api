from fastapi import FastAPI
import uvicorn
from database import engine, Base
from contextlib import asynccontextmanager
from router_api.routers_book import router as router_books
from router_api.routers_author import router as router_authors


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Здесь приложение работает
    yield
    # При завершении приложения можно закрыть соединение (если нужно)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(
    router_books,
    prefix="/books",
    tags=["Books"],
)
app.include_router(
    router_authors,
    prefix="/authors",
    tags=["Authors"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
