import pika


def send_message_to_rabbit(message_text):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='books_queue')

    channel.basic_publish(exchange='', routing_key='books_queue', body=message_text)
    print(f" [x] Sent {message_text}")
    connection.close()
