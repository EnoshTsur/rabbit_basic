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
        # Declare a fanout exchange
        channel.exchange_declare(
            exchange=LOGS_EXCHANGE,  # Exchange name
            exchange_type='fanout',  # Type of exchange
            durable=True  # Ensures exchange is durable
        )

        # Publish the message to the fanout exchange
        channel.basic_publish(
            exchange=LOGS_EXCHANGE,  # Publish to the fanout exchange
            routing_key='',  # Routing key is ignored for fanout
            body=message.encode()  # Encode the message to bytes
        )

        # Log confirmation
        print(f" [x] Sent: {message}")
