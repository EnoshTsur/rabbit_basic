from app.rabbit.channel import create_channel
from app.settings.config import ENOSH_QUEUE, DIRECT_EXCHANGE, DIRECT_QUEUE, ROUTING_KEY


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


def publish_direct(message: str):
    with create_channel() as channel:
        # Declare a direct exchange
        channel.exchange_declare(
            exchange=DIRECT_EXCHANGE,  # Exchange name
            exchange_type='direct',  # Type of exchange
            durable=True  # Make the exchange persistent
        )

        # Declare a durable queue
        channel.queue_declare(
            queue=DIRECT_QUEUE,
            durable=True,
            arguments={
                "x-max-length": 1000,  # Limit the queue to 1000 messages
                "x-message-ttl": 60000  # Messages expire after 60,000 ms (1 minute)
            }
        )

        # Bind the queue to the exchange with a routing key
        channel.queue_bind(
            queue=DIRECT_QUEUE,  # Queue name
            exchange=DIRECT_EXCHANGE,  # Exchange name
            routing_key=ROUTING_KEY  # Routing key for direct routing
        )

        # Publish the message to the direct exchange
        channel.basic_publish(
            exchange=DIRECT_EXCHANGE,  # Publish to the direct exchange
            routing_key=ROUTING_KEY,  # Routing key for routing
            body=message.encode()  # Encode the message to bytes
        )

        # Log confirmation
        print(f" [x] Sent: {message}")
