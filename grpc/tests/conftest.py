import datetime

import psycopg2
import pytest

import settings


@pytest.fixture
def db_connection():
    conn = psycopg2.connect(
            database=settings.DB_NAME_TEST,
            user=settings.DB_USER_TEST,
            password=settings.DB_PASSWORD_TEST,
            host=settings.DB_HOST_TEST,
            port=settings.DB_PORT_TEST
        )
    conn.autocommit = True
    return conn


@pytest.fixture(scope="function", autouse=True)
def clean_tables(db_connection):
    """Clean data in all tables before running test function"""
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE books CASCADE;")


@pytest.fixture(scope="function")
def create_book(db_connection):
    def create_book_in_db(title, author):
        with db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO books (title, author, publish_date) VALUES (%s, %s, %s) RETURNING id",
                    (title, author, datetime.date.today())
                )
                id_of_new_row = cursor.fetchone()[0]
        return id_of_new_row
    return create_book_in_db
