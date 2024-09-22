import asyncio
from typing import Any, AsyncGenerator
from typing import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from starlette.testclient import TestClient

from database_interaction import get_db, metadata
from models import Book, Base, User
from hashing import Hasher
from main import app
from settings import TEST_DATABASE_URL

CLEAN_TABLES = [
    "users",
    "books"
]


engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session")
async def async_session_test():
    yield async_session_maker


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def get_user_from_database(async_session_test):
    async def get_user_from_database_by_username(username: str):
        async with async_session_test() as session:
            user_row = await session.execute(
                text("SELECT * FROM users WHERE username = :un;"), {"un": username}
            )
            if user := user_row.fetchall()[0]:
                return user

    return get_user_from_database_by_username


@pytest.fixture
async def create_book(async_session_test):
    async def create_book_in_db(title, author, publish_date):
        async with async_session_test() as session:
            new_book = Book(
                title=title,
                author=author,
                publish_date=publish_date,
            )
            session.add(new_book)
            await session.commit()
        return new_book
    return create_book_in_db


@pytest.fixture
async def create_user(async_session_test):
    async def create_user_in_db(username: str, password: str):
        password = Hasher.get_password_hash(password)
        new_user = User(
            username=username,
            password=password
        )
        async with async_session_test() as session:
            session.add(new_user)
            await session.commit()
        return new_user

    return create_user_in_db
