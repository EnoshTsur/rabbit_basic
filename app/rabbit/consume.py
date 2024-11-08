from pika.adapters.blocking_connection import BlockingChannel

def consume_messages(channel: BlockingChannel, method, props, body):
    print(body)
    channel.basic_ack(method.delivery_tag)
