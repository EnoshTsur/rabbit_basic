from app.rabbit.channel import create_channel
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


def publish_log(message: str):
    with create_channel() as channel:
        # The fanout exchange is very simple. As you can probably guess from the name,
        # it just broadcasts all the messages it receives to all the queues it knows.
        # And that's exactly what we need for our logger.
        channel.exchange_declare(
            exchange=LOG_TOPIC_EXCHANGE,
            exchange_type='fanout',
            durable=True
        )

        # Whenever we connect to Rabbit we need a fresh, empty queue.
        # To do it we could create a queue with a random name, or, even better -
        # let the server choose a random queue name for us.
        # We can do this by supplying empty queue parameter to queue_declare:
        # once the consumer connection is closed, the queue should be deleted.
        # There's an exclusive flag for that:
        result = channel.queue_declare(queue='',exclusive=True)

        # We've already created a fanout exchange and a queue.
        # Now we need to tell the exchange to send messages to our queue.
        # That relationship between exchange and a queue is called a binding.
        channel.queue_bind(exchange=LOG_TOPIC_EXCHANGE, queue=result.method.queue)

        # Publish the message
        channel.basic_publish(
            exchange=LOG_TOPIC_EXCHANGE,
            routing_key='',
            body=message.encode()
        )

        print(f" [x] Sent: {message}")