from fastapi import APIRouter

from .books import books_router
from .users import user_router

main_api_router = APIRouter(prefix="/api")
main_api_router.include_router(books_router, prefix="/books", tags=["Книги"])
main_api_router.include_router(user_router, prefix="/users", tags=["Пользователи"])
