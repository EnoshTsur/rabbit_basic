import sys
from app.rabbit.channel import create_channel
from app.rabbit.consume import consume_messages
from app.settings.config import LOGS_EXCHANGE

if __name__ == '__main__':
    try:
        with create_channel() as channel:
            channel.exchange_declare(
                exchange=LOGS_EXCHANGE,
                exchange_type='fanout',
                durable=True
            )
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=LOGS_EXCHANGE, queue=queue_name)
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=consume_messages,
                auto_ack=False  # Make sure to acknowledge messages
            )
            channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
