import sys
from app.rabbit.channel import create_channel
from app.rabbit.consume import consume_messages
from app.settings.config import ENOSH_QUEUE

if __name__ == '__main__':
    try:
        with create_channel() as channel:
            channel.basic_consume(ENOSH_QUEUE, consume_messages)
            channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
