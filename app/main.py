import sys
from app.rabbit.channel import create_channel
from app.rabbit.consume import consume_messages
from app.settings.config import TOPIC_EXCHANGE, LOG_INFO_ROUTING_KEY, LOG_INFO_QUEUE

if __name__ == '__main__':
    try:
        with create_channel() as channel:
            # Declare the fanout exchange
            channel.exchange_declare(
                exchange=TOPIC_EXCHANGE,  # Exchange name
                exchange_type='topic',  # Type of exchange
                durable=True  # Ensure exchange durability
            )

            # Declare a queue (let RabbitMQ generate a unique name)
            channel.queue_declare(queue=LOG_INFO_QUEUE, durable=True)

            # Bind the queue to the direct exchange
            channel.queue_bind(
                exchange=TOPIC_EXCHANGE,
                queue=LOG_INFO_QUEUE,
                routing_key=LOG_INFO_ROUTING_KEY
            )

            print(f" [*] Waiting for logs in queue: {LOG_INFO_QUEUE}.")

            # Consume messages from the queue
            channel.basic_consume(
                queue=LOG_INFO_QUEUE,
                on_message_callback=consume_messages,
                auto_ack=False  # Automatically acknowledge the message
            )

            # Start listening for messages
            channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
