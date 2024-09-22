from concurrent import futures
import grpc
import pytest

from books import books_pb2
from books import books_pb2_grpc
from books.books_server import BooksService


class TestBooks:
    server_class = BooksService
    port = 50051

    @pytest.fixture(autouse=True)
    def setup(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        books_pb2_grpc.add_BooksServicer_to_server(self.server_class(), self.server)
        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()

    def teardown(self):
        self.server.stop(None)

    def test_single_book(self, create_book):
        book_id = create_book(title='Test Book', author='Test Author')
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = books_pb2_grpc.BooksStub(channel)
            response = stub.SingleBook(books_pb2.SingleBookRequest(book_id=book_id))
        assert response.book.title == 'Test Book'
        assert response.book.author == 'Test Author'

    def test_multiple_books(self, create_book):
        for index in range(11):
            create_book(title=f'Test Book {index}', author=f'Test Author {index}')
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = books_pb2_grpc.BooksStub(channel)
            response = stub.BookList(books_pb2.BookListRequest(page=1, limit=10))
        assert len(response.books) == 10
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = books_pb2_grpc.BooksStub(channel)
            response = stub.BookList(books_pb2.BookListRequest(page=3, limit=10))
        assert len(response.books) == 0
