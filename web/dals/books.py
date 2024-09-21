from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import update, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book
from schemas import BookToCreate, BookToUpdate


class BookDAL:
    not_found_exception = HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Книга не найдена",
    )
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_book(self, book_data: BookToCreate) -> Book:
        new_book = Book(**book_data.model_dump())
        self.db_session.add(new_book)
        await self.db_session.commit()
        return new_book

    async def get_book(self, book_id: int) -> Book:
        book = select(Book).where(Book.id == book_id)
        result = await self.db_session.execute(book)
        book = result.scalar_one_or_none()
        if not book:
            raise self.not_found_exception
        return book

    async def update_book(self, book_id: int, book_data: BookToUpdate) -> Book:
        query = (
            update(Book)
            .where(Book.id == book_id)
            .values(**book_data.model_dump(exclude_unset=True))
            .returning(Book)
        )
        result = await self.db_session.execute(query)
        book = result.scalar_one_or_none()
        if not book:
            raise self.not_found_exception
        return book

    async def delete_book(self, book_id: int) -> None:
        query = (
            delete(Book)
            .where(Book.id == book_id)
            .returning(Book.id)
        )
        result = await self.db_session.execute(query)
        if not result.scalar_one_or_none():
            raise self.not_found_exception

    async def books_list(self, page: int = 1, limit: int = 20) -> tuple[int, list[Book]]:
        count_query = select(func.count(Book.id))
        count_result = await self.db_session.execute(count_query)
        count = count_result.scalar_one_or_none()
        query = (
            select(Book)
            .limit(limit)
            .offset((page - 1) * limit)
        )
        result = await self.db_session.execute(query)
        return count, list(result.scalars())
