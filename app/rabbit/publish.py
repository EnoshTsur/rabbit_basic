from app.rabbit.channel import create_channel
from app.rabbit.exchange import LogLevel
from app.settings.config import ENOSH_QUEUE, LOG_TOPIC_EXCHANGE


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


def publish_log(message: str, log_level: LogLevel):
    with create_channel() as channel:
        channel.exchange_declare(
            exchange=LOG_TOPIC_EXCHANGE,
            exchange_type='topic',
            durable=True
        )

        # Declare the queue
        channel.queue_declare(
            queue=ENOSH_QUEUE,
            durable=True
        )

        # Bind queue to exchange with routing patterns
        # This ensures the queue receives messages for all log patterns
        for pattern in ["log.info", "log.error", "log.all"]:
            channel.queue_bind(
                queue=ENOSH_QUEUE,
                exchange=LOG_TOPIC_EXCHANGE,
                routing_key=pattern
            )

        # Publish the message
        channel.basic_publish(
            exchange=LOG_TOPIC_EXCHANGE,
            routing_key=log_level.value,
            body=message.encode()
        )

        print(f" [x] Sent {log_level.value}: {message}")