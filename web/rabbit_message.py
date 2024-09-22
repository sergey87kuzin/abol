import logging

import pika


def send_message_to_rabbit(message_text):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('172.21.0.2'))
    except pika.exceptions.AMQPConnectionError:
        logging.error("RabbitMQ connection failed")
        return
    channel = connection.channel()

    channel.queue_declare(queue='books_queue', arguments={'x-max-length': 100})

    channel.basic_publish(exchange='', routing_key='books_queue', body=message_text)
    logging.info(f" [x] Sent {message_text}")
    connection.close()
