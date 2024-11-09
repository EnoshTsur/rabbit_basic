from app.rabbit.channel import create_channel
from app.settings.config import ENOSH_QUEUE, DIRECT_EXCHANGE, DIRECT_QUEUE, ROUTING_KEY, TOPIC_EXCHANGE, \
    LOGS_INFO_QUEUE, LOGS_ERROR_QUEUE, LOGS_ALL_QUEUE, LOG_INFO_ROUTING_KEY, LOG_ERROR_ROUTING_KEY, LOG_ALL_ROUTING_KEY


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


def publish_topic(message: str, routing_key: str):
    with create_channel() as channel:
        # Declare a topic exchange
        channel.exchange_declare(
            exchange=TOPIC_EXCHANGE,  # Exchange name
            exchange_type='topic',  # Type of exchange
            durable=True  # Make the exchange persistent
        )

        # Declare queues for different log levels
        channel.queue_declare(queue=LOGS_INFO_QUEUE, durable=True)
        channel.queue_declare(queue=LOGS_ERROR_QUEUE, durable=True)
        channel.queue_declare(queue=LOGS_ALL_QUEUE, durable=True)

        for key, queue in [
            (LOG_INFO_ROUTING_KEY, LOGS_INFO_QUEUE),
            (LOG_ERROR_ROUTING_KEY, LOGS_ERROR_QUEUE),
            (LOG_ALL_ROUTING_KEY, LOGS_ALL_QUEUE)
        ]:
            channel.queue_bind(
                queue=queue,
                exchange=TOPIC_EXCHANGE,
                routing_key=key  # Matches exactly 'logs.info'
            )

        # Publish the message to the topic exchange
        channel.basic_publish(
            exchange=TOPIC_EXCHANGE,  # Publish to the topic exchange
            routing_key=routing_key,  # Routing key determines the target queue(s)
            body=message.encode()  # Encode the message to bytes
        )

        # Log confirmation
        print(f" [x] Sent: '{message}' with routing key '{routing_key}'")