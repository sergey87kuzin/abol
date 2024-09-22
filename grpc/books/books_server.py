import threading
from concurrent import futures

import grpc
import pika

from books import books_pb2_grpc, books_pb2
from books.books_reading_service import BooksReadingService


class BooksService(books_pb2_grpc.BooksServicer):
    def SingleBook(self, request, context):
        book = BooksReadingService().get_book(book_id=request.book_id)
        if not book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found!')
            return books_pb2.SingleBookResponse()
        return books_pb2.SingleBookResponse(book=book)

    def BookList(self, request, context):
        page = request.page
        limit = request.limit
        if page == 0:
            page = 1
        if limit == 0:
            limit = 10
        if page < 0 or limit < 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Wrong page or limit!')
            return books_pb2.BookListResponse()
        books = BooksReadingService().get_books(page=page, limit=limit)
        return books_pb2.BookListResponse(books=books)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BooksServicer_to_server(
        BooksService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


def rabbit() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    threading.Thread(target=rabbit, name="rabbit_thread", daemon=True).start()
    serve()
