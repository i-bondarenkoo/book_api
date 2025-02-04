from fastapi import FastAPI
import uvicorn
from database import engine, Base
from contextlib import asynccontextmanager
from routers import router as router_books


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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
