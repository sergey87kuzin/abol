from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database_interaction import get_db
from handlers import (
    create_new_book_handler, delete_book_handler, get_book_handler, get_books_list_handler, update_book_handler,
)
from handlers.auth import check_user_auth
from pagination import PagedResponseSchema, PageParams
from rabbit_message import send_message_to_rabbit
from schemas import BookToCreate, BookToShow, BookToUpdate

SessionDep = Annotated[AsyncSession, Depends(get_db)]
UserDep = Depends(check_user_auth)

books_router = APIRouter(dependencies=[UserDep])


@books_router.get(
    "/",
    response_model=PagedResponseSchema,
    summary="Список книг",
    description="Получение списка книг с пагинацией"
)
async def books_list(page_params: Annotated[PageParams, Query()], session: SessionDep):
    return await get_books_list_handler(page_params, session)


@books_router.post(
    "/",
    response_model=BookToShow,
    summary="Создание книги",
    description="Создание книги по названию и автору, указывать дату публикации необязательно"
)
async def book_create(book: BookToCreate, session: SessionDep):
    new_book = await create_new_book_handler(book, session)
    send_message_to_rabbit(f"New book created: {new_book.id}")
    return new_book


@books_router.get(
    "/{book_id}/",
    response_model=BookToShow,
    summary="Экземпляр книги",
    description="Получение данных о книге по ее id"
)
async def book_show(book_id: int, session: SessionDep):
    return await get_book_handler(book_id, session)


@books_router.delete(
    "/{book_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление книги",
    description="Удаление книги по ее id"
)
async def book_delete(book_id: int, session: SessionDep):
    await delete_book_handler(book_id, session)
    send_message_to_rabbit(f"Book deleted: {book_id}")


@books_router.patch(
    "/{book_id}/",
    response_model=BookToShow,
    summary="Изменение книги",
    description="Изменение данных о книге"
)
async def book_update(book_id: int, book: BookToUpdate, session: SessionDep):
    updated_book = await update_book_handler(book_id, book, session)
    send_message_to_rabbit(f"Book updated: {book_id}")
    return updated_book
