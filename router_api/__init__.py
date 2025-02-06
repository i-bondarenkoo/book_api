# router_api/__init__.py

from .routers_book import router as books_router
from .routers_author import router as authors_router

__all__ = ["books_router", "authors_router"]
