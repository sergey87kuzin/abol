from sqlalchemy.ext.asyncio import AsyncSession

from dals.books import BookDAL
from pagination import PagedResponseSchema, PageParams, paginate
from schemas import BookToCreate, BookToShow, BookToUpdate

__all__ = (
    "create_new_book_handler",
    "get_book_handler",
    "update_book_handler",
    "delete_book_handler",
    "get_books_list_handler"
)


async def create_new_book_handler(body: BookToCreate, session: AsyncSession) -> BookToShow:
    # Возможно, имеет смысл перед созданием проверять на уникальность пару название-автор
    # Но это ведь могут быть разные издания и т.п. Так что вопрос дискуссионный
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.create_book(body)
    return BookToShow.model_validate(book, from_attributes=True)


async def get_book_handler(book_id: int, session: AsyncSession) -> BookToShow:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.get_book(book_id)
    return BookToShow.model_validate(book, from_attributes=True)


async def update_book_handler(book_id: int, body: BookToUpdate, session: AsyncSession) -> BookToShow:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.update_book(book_id, body)
    return BookToShow.model_validate(book, from_attributes=True)


async def delete_book_handler(book_id: int, session: AsyncSession) -> None:
    async with session.begin():
        book_dal = BookDAL(session)
        await book_dal.delete_book(book_id)


async def get_books_list_handler(page_params: PageParams, session: AsyncSession) -> PagedResponseSchema:
    async with session.begin():
        book_dal = BookDAL(session)
        count, books = await book_dal.books_list(**page_params.model_dump())
    return await paginate(
        count=count,
        objects=books,
        page_params=page_params,
        response_model=BookToShow
    )
