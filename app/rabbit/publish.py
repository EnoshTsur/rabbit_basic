from app.rabbit.channel import create_channel
from app.settings.config import ENOSH_QUEUE, LOGS_EXCHANGE


def publish_message(message: str):
    with create_channel() as channel:
        # Declare the queue (idempotent - will only create if doesn't exist)
        channel.queue_declare(queue=ENOSH_QUEUE, durable=True)
        # Publish the message
        channel.basic_publish(
            exchange='',  # Empty exchange for direct queue publishing
            routing_key=ENOSH_QUEUE,
            body=message.encode()
        )

        print(f" [x] Sent message: {message}")


def publish_log(message: str):
    with create_channel() as channel:
        # The fanout exchange is very simple. As you can probably guess from the name,
        # it just broadcasts all the messages it receives to all the queues it knows.
        # And that's exactly what we need for our logger.
        channel.exchange_declare(
            exchange=LOGS_EXCHANGE,
            exchange_type='fanout',
            durable=True
        )

        # Publish the message
        channel.basic_publish(
            exchange=LOGS_EXCHANGE,
            routing_key='',
            body=message.encode()
        )

        print(f" [x] Sent: {message}")