import psycopg2
import psycopg2.extras

import settings


class BooksReadingService:
    def __init__(self):
        self.connect = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )

    def get_books(self, page, limit):
        with self.connect:
            with self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """SELECT id, title, author, publish_date FROM books OFFSET %s LIMIT %s""",
                    ((page - 1) * limit, limit)
                )
                books = cursor.fetchall()
        messages = []
        for book in books:
            book["publish_date"] = book["publish_date"].strftime("%Y-%m-%d")
            messages.append(book)
        return messages

    def get_book(self, book_id):
        with self.connect:
            with self.connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """SELECT id, title, author, publish_date FROM books WHERE id = %s""",
                    (book_id,)
                )
                book = cursor.fetchone()
        if book:
            book["publish_date"] = book["publish_date"].strftime("%Y-%m-%d")
            return book
