from pika import PlainCredentials, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.connection import ConnectionParameters
import toolz as t

connection: BlockingConnection = t.pipe(
    PlainCredentials("guest", "guest"),
    lambda credentials: ConnectionParameters(credentials=credentials),
    BlockingConnection
)

channel = connection.channel()

queue_name = "pika_queue"

def consume_messages(channel: BlockingChannel, method, props, body):
    print(body)
    channel.basic_ack(method.delivery_tag)

if __name__ == '__main__':
    channel.basic_consume(queue_name, consume_messages)
    channel.start_consuming()